"""
Robbor Command – Centralized dashboard & REST API for fluidic coupling status.
Reports Capped / Exposed / Warning state of every fluid line in the cluster.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Robbor Command API",
    description="Telemetry and control plane for Robbor CP intelligent fluidic coupling protection.",
    version="1.0.0",
)


class CapState(str, Enum):
    EXPOSED = "EXPOSED"
    SECURE = "SECURE"
    WARNING_CONTAMINATED = "WARNING_CONTAMINATED"


class PortStatus(BaseModel):
    port_id: str = Field(..., description="Unique identifier of the UQD port / cap node")
    rack_id: str
    gpu_node: Optional[str] = None
    state: CapState
    moisture_index: float = Field(ge=0.0, le=1.0)
    last_seen: datetime
    temperature_c: Optional[float] = None


class PortUpdate(BaseModel):
    state: CapState
    moisture_index: float = Field(ge=0.0, le=1.0)
    temperature_c: Optional[float] = None


# In-memory store for demonstration / single-node deployment
_ports: Dict[str, PortStatus] = {}


def _seed_demo_data() -> None:
    now = datetime.now(timezone.utc)
    demo = [
        PortStatus(
            port_id="UQD-R01-G0-IN",
            rack_id="RACK-01",
            gpu_node="GPU-0",
            state=CapState.SECURE,
            moisture_index=0.08,
            last_seen=now,
            temperature_c=38.2,
        ),
        PortStatus(
            port_id="UQD-R01-G0-OUT",
            rack_id="RACK-01",
            gpu_node="GPU-0",
            state=CapState.SECURE,
            moisture_index=0.11,
            last_seen=now,
            temperature_c=41.5,
        ),
        PortStatus(
            port_id="UQD-R02-G3-IN",
            rack_id="RACK-02",
            gpu_node="GPU-3",
            state=CapState.EXPOSED,
            moisture_index=0.0,
            last_seen=now,
            temperature_c=None,
        ),
        PortStatus(
            port_id="UQD-R03-G1-IN",
            rack_id="RACK-03",
            gpu_node="GPU-1",
            state=CapState.WARNING_CONTAMINATED,
            moisture_index=0.82,
            last_seen=now,
            temperature_c=67.4,
        ),
    ]
    for p in demo:
        _ports[p.port_id] = p


_seed_demo_data()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "robbor-command", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/v1/ports", response_model=List[PortStatus])
def list_ports(rack_id: Optional[str] = None, state: Optional[CapState] = None) -> List[PortStatus]:
    results = list(_ports.values())
    if rack_id:
        results = [p for p in results if p.rack_id == rack_id]
    if state:
        results = [p for p in results if p.state == state]
    return results


@app.get("/api/v1/ports/{port_id}", response_model=PortStatus)
def get_port(port_id: str) -> PortStatus:
    if port_id not in _ports:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Port not found")
    return _ports[port_id]


@app.put("/api/v1/ports/{port_id}", response_model=PortStatus)
def update_port(port_id: str, update: PortUpdate) -> PortStatus:
    if port_id not in _ports:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Port not found")
    existing = _ports[port_id]
    existing.state = update.state
    existing.moisture_index = update.moisture_index
    existing.temperature_c = update.temperature_c
    existing.last_seen = datetime.now(timezone.utc)
    _ports[port_id] = existing
    return existing


@app.post("/api/v1/ports", response_model=PortStatus, status_code=status.HTTP_201_CREATED)
def register_port(port: PortStatus) -> PortStatus:
    if port.port_id in _ports:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Port already registered")
    port.last_seen = datetime.now(timezone.utc)
    _ports[port.port_id] = port
    return port


@app.get("/api/v1/summary")
def cluster_summary() -> dict:
    total = len(_ports)
    by_state = {s.value: 0 for s in CapState}
    for p in _ports.values():
        by_state[p.state.value] += 1
    return {
        "total_ports": total,
        "by_state": by_state,
        "critical_count": by_state[CapState.EXPOSED.value] + by_state[CapState.WARNING_CONTAMINATED.value],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    """Minimal operator dashboard."""
    summary = cluster_summary()
    rows = ""
    for p in sorted(_ports.values(), key=lambda x: x.port_id):
        color = {
            CapState.SECURE: "#22c55e",
            CapState.EXPOSED: "#ef4444",
            CapState.WARNING_CONTAMINATED: "#f59e0b",
        }[p.state]
        rows += f"""
        <tr>
          <td>{p.port_id}</td>
          <td>{p.rack_id}</td>
          <td>{p.gpu_node or '—'}</td>
          <td style="color:{color};font-weight:600">{p.state.value}</td>
          <td>{p.moisture_index:.2f}</td>
          <td>{p.temperature_c if p.temperature_c is not None else '—'}</td>
          <td>{p.last_seen.strftime('%Y-%m-%d %H:%M:%S UTC')}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Robbor Command</title>
  <style>
    :root {{ font-family: system-ui, -apple-system, sans-serif; }}
    body {{ margin: 0; background: #0f172a; color: #e2e8f0; }}
    header {{ background: #1e293b; padding: 1rem 2rem; border-bottom: 1px solid #334155; }}
    h1 {{ margin: 0; font-size: 1.4rem; }}
    .stats {{ display: flex; gap: 1.5rem; padding: 1.5rem 2rem; }}
    .card {{ background: #1e293b; border-radius: 8px; padding: 1rem 1.25rem; min-width: 120px; }}
    .card .val {{ font-size: 1.8rem; font-weight: 700; }}
    .card .lbl {{ font-size: 0.8rem; color: #94a3b8; }}
    table {{ width: calc(100% - 4rem); margin: 0 2rem 2rem; border-collapse: collapse; }}
    th, td {{ text-align: left; padding: 0.6rem 0.8rem; border-bottom: 1px solid #334155; }}
    th {{ color: #94a3b8; font-weight: 500; font-size: 0.85rem; }}
    a {{ color: #38bdf8; }}
  </style>
</head>
<body>
  <header>
    <h1>Robbor Command — Fluidic Coupling Telemetry</h1>
  </header>
  <div class="stats">
    <div class="card"><div class="val">{summary['total_ports']}</div><div class="lbl">Total Ports</div></div>
    <div class="card"><div class="val" style="color:#22c55e">{summary['by_state']['SECURE']}</div><div class="lbl">Secure</div></div>
    <div class="card"><div class="val" style="color:#ef4444">{summary['by_state']['EXPOSED']}</div><div class="lbl">Exposed</div></div>
    <div class="card"><div class="val" style="color:#f59e0b">{summary['by_state']['WARNING_CONTAMINATED']}</div><div class="lbl">Contaminated</div></div>
    <div class="card"><div class="val">{summary['critical_count']}</div><div class="lbl">Critical</div></div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Port ID</th><th>Rack</th><th>GPU Node</th><th>State</th>
        <th>Moisture</th><th>Temp °C</th><th>Last Seen</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
  <p style="margin:0 2rem 2rem;color:#64748b;font-size:0.85rem">
    API docs: <a href="/docs">/docs</a> · Health: <a href="/health">/health</a>
  </p>
</body>
</html>"""
