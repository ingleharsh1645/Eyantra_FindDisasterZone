# Eyantra_FindDisasterZone - Task 1

Solution for disaster zone detection and drone simulation using ROS 2, Python, and OpenCV as part of the e-Yantra Robotics Competition.

---

## 📌 Features
* **Disaster Zone Detection:** Image processing using OpenCV to identify target areas.
* **Drone Simulation:** Autonomous navigation and waypoints execution in Gazebo/ROS 2.
* **Custom Nodes:** Modular ROS 2 nodes for perception and control.

---

## 🛠️ Prerequisites & Dependencies
Make sure you have the following installed:
* **OS:** Ubuntu 22.04 LTS
* **ROS Version:** ROS 2 Humble
* **Python Dependencies:**
  ```bash
  pip install opencv-python numpy
  ```
  ---

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/ingleharsh1645/Eyantra_FindDisasterZone.git
   cd Eyantra_FindDisasterZone
   ```
   
 2. **Build the ROS 2 workspace:**
   ```bash
   colcon build
   source install/setup.bash
  ```
   ---
   
## 🎮 How to Run Task 1 
  1. **Launch the Simulation Environment**
  ```
   ros2 launch <package_name> <launch_file>.launch.py
  ```
   
  2. **Run the Task 1 Detection / Control Node**
   ```
   ros2 run <package_name> <node_name>
   ```
   ---

   ## 📁 Project Structure 
   ``` text
   Eyantra_FindDisasterZone/
├── launch/             # ROS launch files
├── scripts/            # Python nodes and scripts
├── config/             # YAML configurations
├── CMakeLists.txt / setup.py
└── README.md
 ```

---

## Ubuntu Setup :

1.**Dependencies (OpenCV & NumPy) Install**
```
sudo apt update
sudo apt install python3-opencv python3-numpy
```
2. **e-Yantra Repository**
```
mkdir -p ~/pico_ws/src
cd ~/pico_ws/src
git clone -b kd_sim https://github.com/eYantra-Robotics-Competition/eYRC_26-27_Khojo-Drone.git --recursive .
cd ~/pico_ws
colcon build
source install/setup.bash

```
---
 

   
  
