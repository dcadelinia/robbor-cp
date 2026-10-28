# Hardware – Robbor CP Node

This directory contains the physical design assets for the Robbor CP intelligent fluidic coupling cap.

## Layout

| Path | Description |
|------|-------------|
| `cad/` | 3D CAD models (STEP / STL) of the injection-molded housing and locking collar |
| `schematics/` | KiCad project for the custom circular low-power PCB (sensor array + BLE/NFC) |

## Material & Mechanical Notes

- Housing: CNT-filled PEEK or equivalent ESD-dissipative fluoropolymer (10⁵–10⁹ Ω/sq)
- Operating temperature: −20 °C to +85 °C
- Mating cycles: ≥ 5 000
- Seal: dual-lip elastomer + capillary-barrier micro-pore matrix (r < 2.5 µm)

> **Note:** Production STEP and KiCad source files are under controlled release.
> Contact the repository maintainers or use the Nvidia Inception Capital Connect data room for access.
