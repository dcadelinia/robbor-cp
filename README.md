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
### 🟢 Nvidia Inception Ecosystem Integration Matrix

Robbor CP is engineered to natively interface with the enterprise Nvidia data center and edge compute stacks to automate physical layer protection and risk management. 

### 1. Edge Auditing via Nvidia DeepStream & Jetson Orin

The edge-jetson/ directory houses the real-time computer vision configuration. By deploying optimized TensorRT inference engines onto on-site Nvidia Jetson Orin modules, the system dynamically analyzes infrastructure visual data feeds (via RTSP streams) to instantly detect, categorize, and flag un-mated or exposed UQD port connections. 

### 2. Predictive Thermal Throttling via Nvidia DCGM

The rack-egx/ architecture utilizes the Nvidia Data Center GPU Manager (DCGM) API to establish a tight feedback loop between physical state changes and GPU thermals. In the event of fluidic loop anomalies or localized micron-scale microchannel clogs caused by physical interface contamination, the Go-based monitoring daemon intercepts junction temperature spikes and triggers emergency node isolation commands via Nvidia Base Command.
