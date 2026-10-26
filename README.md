# robbor-cp
Intelligent fluidic coupling protection and telemetry for next-generation AI data center architecture.
### Robbor CP (Cooling Protection)

Robbor CP is an intelligent, telemetry-enabled hardware protection system designed specifically for Universal Quick Disconnect (UQD) fluid couplings in liquid-cooled AI data centers. 

Optimized for high-density environments like the Nvidia Blackwell and Rubin architectures, Robbor CP bridges the gap between passive physical dust covers and active digital asset management. 

### 🚀 Key Features

* **Smart Port Telemetry:** Integrated low-power wireless signaling (NFC/BLE) that communicates port exposure status to the rack infrastructure in real-time.
* **ESD-Safe Polymer Shielding:** Advanced static-dissipating housing prevents high-voltage discharge near high-bandwidth memory (HBM) banks.
* **Moisture-Sensing Core:** Internal electronic grid detects microscopic coolant micro-leaks or high-humidity ingress before hardware is hot-swapped.
* **Rugged Mechanical Seal:** Industrial-grade locking mechanism designed for thousands of deployment cycles in ambient temperatures up to 85°C.

### ⚙️ Architecture Overview

Robbor CP operates on a three-tier hardware-to-software architecture: 

1. **Robbor CP Node (Hardware):** The physical cap embedded with an ultra-low-power microchip and sensor array.
2. **Robbor-Link (Firmware/Daemon):** A lightweight background service running on the server rack management controller (BMC) that listens for cap states.
3. **Robbor Command (Software API):** A centralized dashboard reporting the exact status (Capped, Exposed, Warning) of every fluid line in the cluster.

### 📁 Repository Directory

* /hardware: Contains 3D CAD files (.STEP) for the physical injection-molded cap and KiCad electrical schematics for the custom circular PCB.
* /firmware: Source code for the internal ultra-low-power microcontroller.
* /software: Python-based REST API and web dashboard for data center technicians.
