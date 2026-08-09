# GeoVision - Integrated Geospatial Visualization and Analysis Platform

GeoVision is an offline desktop-based geospatial visualization and analysis platform developed using **Python** and **PySide6**.

The application provides an interactive environment for loading, visualizing, and exploring spatial data through maps, terrain visualization, trajectory playback, multi-video monitoring, and view-geometry visualization.

The project follows a modular architecture in which data providers, visualization widgets, terrain processing, trajectory playback, and the graphical user interface are maintained as separate components.

---

## ✨ Key Features

- 🗺️ Interactive 2D geospatial map visualization
- ⛰️ 3D terrain visualization using elevation data
- 📍 Spatial data-source and object visualization
- 📐 View geometry visualization
- 🛣️ Trajectory and path visualization
- ▶️ Trajectory playback and animation
- 🎥 Multi-video monitoring interface
- 📊 Excel-based data loading
- 📋 Data summary and object information panels
- ⚙️ Configurable data-source settings
- 🧭 Coordinate and elevation information
- 📴 Offline-first visualization workflow
- 🧩 Modular Python architecture
- 🖥️ Desktop GUI built with PySide6

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| PySide6 | Desktop graphical user interface |
| Qt Multimedia | Local video playback |
| Pandas | Tabular data processing |
| NumPy | Numerical processing |
| OpenPyXL | Excel file processing |
| PyVista | 3D visualization |
| Rasterio | DEM and raster processing |
| PyProj | Coordinate transformation |
| Pillow | Image processing |
| Leaflet | Interactive 2D map visualization |
| HTML / JavaScript | Map interface |
| Git | Version control |
| GitHub | Source-code repository |

---

## 🖥️ Application Overview

GeoVision combines multiple visualization and data-processing components into a single desktop application.

The main interface provides access to:

1. **Data Sources**
2. **Video Viewer**
3. **Data Summary**
4. **Spatial Visualization**
5. **2D Map**
6. **3D Terrain**
7. **Trajectory Playback**
8. **View Geometry**
9. **Activity Log**

The application is designed to allow users to load sample datasets and interactively explore the resulting spatial information.

---

## 🎯 Project Objectives

The primary objectives of GeoVision are:

- Provide a unified desktop interface for geospatial visualization.
- Display spatial information in an intuitive graphical environment.
- Support both 2D and 3D visualization.
- Visualize elevation and terrain information.
- Display trajectories and their movement over time.
- Provide an organized multi-video monitoring interface.
- Separate data processing from the graphical interface.
- Support offline operation using locally available resources.
- Maintain a modular and extensible software architecture.

---

## 🔄 Basic Application Workflow

```text
                    +----------------------+
                    |       GeoVision       |
                    |   Desktop Application|
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                |                |
              ▼                ▼                ▼
         Load Data         Load Path      Load View Data
              |                |                |
              ▼                ▼                ▼
       Excel Provider     Trajectory        FOV Provider
                           Provider
              |                |                |
              +----------------+----------------+
                               |
                               ▼
                    +----------------------+
                    |   Application Data   |
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                |                |
              ▼                ▼                ▼
           2D Map         3D Terrain      Video Viewer
              |                |                |
              +----------------+----------------+
                               |
                               ▼
                       Activity / Status
```
# 📁 Project Structure

GeoVision follows a modular project structure. Each directory is responsible for a specific part of the application, making the project easier to develop, maintain, and extend.

```text
GeoVision/
│
├── core/
│   └── Core application components
│
├── data/
│   └── Sample and development data
│
├── dialogs/
│   └── GUI dialog windows
│
├── maps/
│   └── 2D map resources
│
├── models/
│   └── Application data models
│
├── providers/
│   ├── excel_provider.py
│   ├── fov_provider.py
│   ├── mission_data.py
│   └── trajectory_provider.py
│
├── terrain/
│   ├── coordinate_converterr.py
│   ├── dem_loader.py
│   ├── reproject_dem.py
│   ├── terrain_renderer.py
│   └── texture_builder.py
│
├── trajectory/
│   └── trajectory_player.py
│
├── ui/
│   └── main_window.py
│
├── videos/
│   └── Local video samples
│
├── widgets/
│   ├── map_container.py
│   ├── sensor_panel.py
│   ├── video_panel.py
│   └── video_widget.py
│
├── main.py
├── tile_server.py
├── requirements.txt
├── .gitignore
└── README.md
```
# ⚙️ Installation & Setup

Follow the steps below to set up and run GeoVista on a local development machine.

---

## 🖥️ System Requirements

Before installing the project, make sure the following software is available:

- Python 3.10 or newer
- Git
- Windows, Linux, or macOS
- Internet connection for initial dependency installation
- Sufficient storage for optional terrain and video resources

---

## 📥 Clone the Repository

Clone the GeoVista repository using Git:

```bash
git clone https://github.com/SamridhiSehgal/GeoVision-Integrated-Geospatial-Visualization-and-Analysis-Platform.git
```
# ▶️ Running the Application

GeoVision uses two processes for the complete application workflow:

1. **Local Tile Server** for the offline 2D map
   
2. **Main GeoVision Application** for the desktop GUI

Both processes should be running while using the application.

---

## 🗺️ Step 1: Start the Local Tile Server

Open a terminal in the GeoVista project directory.

First, activate the virtual environment.

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```
### Start the tile server in one terminal
```bash
python tile_server.py
```
### Strt the main.py in another terminal
```bash
python main.py
```
# 🧭 Basic Usage

After starting the GeoVista application, the main dashboard provides access to the different visualization and data-processing components.

The typical workflow is:

```text
                    Start GeoVista
                         |
                         ▼
                  Main Dashboard
                         |
          +--------------+--------------+
          |              |              |
          ▼              ▼              ▼
      Load Data      Load Path     Load View Data
          |              |              |
          ▼              ▼              ▼
      Data Panels    Trajectory      View Geometry
          |              |              |
          +--------------+--------------+
                         |
                         ▼
                 Spatial Visualization
                         |
          +--------------+--------------+
          |              |              |
          ▼              ▼              ▼
        2D Map       3D Terrain    Video Viewer
          |              |              |
          +--------------+--------------+
                         |
                         ▼
                  Activity / Status
```
# 🗺️ Visualization Modules

GeoVista combines multiple visualization modules into a single desktop application.

The major visualization components are:

- 🗺️ 2D Map Visualization
- ⛰️ 3D Terrain Visualization
- 🛣️ Trajectory Visualization
- 📐 View Geometry Visualization
- 🎥 Multi-Video Visualization

---

## 🗺️ 2D Map Visualization

The 2D map provides an interactive geographic representation of the loaded spatial data.

The map can display different types of information together, allowing users to explore spatial relationships between the loaded data.

### Supported Map Information

Depending on the input data, the map can display:

- 📍 Data-source locations
- 📍 Object locations
- 🛣️ Trajectory paths
- 📐 View geometry
- 🧭 Geographic coordinates
- ⛰️ Elevation information
- 📏 Spatial distances
- 🗺️ Local map tiles

---

## 🧩 2D Map Workflow

The general map workflow is:

```text
Input Data
    |
    ▼
Data Provider
    |
    ▼
Application Data
    |
    ▼
Map Container
    |
    ▼
Leaflet Map
    |
    ▼
Interactive Visualization
```


## 🖥️ Main Dashboard

The main dashboard provides access to the major GeoVista components.


# 🏗️ Architecture & Data Flow

GeoVista follows a modular architecture that separates the graphical user interface, data processing, visualization, terrain processing, and playback functionality.

This structure makes the application easier to maintain, debug, and extend.

---

## 🧩 High-Level Architecture

The overall architecture can be represented as:

```text
                         +----------------------+
                         |       GeoVista       |
                         |   Desktop GUI        |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                      |                      |
             ▼                      ▼                      ▼
       Data Providers           UI Widgets            Terrain
             |                      |                      |
             ▼                      ▼                      ▼
      Input Processing       Visualization        DEM Processing
             |                      |                      |
             +----------------------+----------------------+
                                    |
                                    ▼
                          Application Data Layer
                                    |
                 +------------------+------------------+
                 |                  |                  |
                 ▼                  ▼                  ▼
              2D Map           3D Terrain         Video Viewer
                 |                  |                  |
                 +------------------+------------------+
                                    |
                                    ▼
                              Main Window
```
