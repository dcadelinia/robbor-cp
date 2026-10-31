# Robbor CP Command API — production image for Fly.io / any container host
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
RUN python -m venv /app/.venv
COPY requirements.txt ./
RUN /app/.venv/bin/pip install --upgrade pip \
 && /app/.venv/bin/pip install -r requirements.txt

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY main.py requirements.txt ./

# Non-root
RUN useradd -r -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Bind 0.0.0.0 so Fly Proxy can reach the process (NOT 127.0.0.1)
# Use uvicorn explicitly — more reliable than `fastapi run` defaults in containers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
