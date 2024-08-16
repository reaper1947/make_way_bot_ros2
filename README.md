# moveo_ros






## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Files and Directories](#files-and-directories)
- [Predefined Movements](#predefined-movements)
- [Known Issues](#known-issues)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Future](#future)

# Installation
Build the Workspace
```

```
# Usage

Running the ROS Nodes

### Fisrt control with Python code
1. Start ROS Master
```

```
2. Run 
```

```
3. Run 
```

```
4. Run 
```

```

### Secound control with terminal
after step 3 you need to run this code on terminal

1. gripper control
```

```
2. Robot control
```

```
also you can see a ``` ``` on terminal real time by this code
``` ```



### Controlling the Arm
You can control the arm using predefined movements for picking and placing objects by entering commands when prompted.

# Files and Directories
- src/moveo_moveit/scripts/
   - ``` ```: Script for controlling the arm to perform pick and place operations.
- urdf/: Contains the URDF model of the BCN3D Moveo.
- launch/: Launch files for starting the MoveIt and ROS nodes.

# Predefined Movements
Predefined movements for picking and placing objects are defined in pick_and_place.py. The script includes trajectories for objects like a box and a cylinder.
```

```




# Known Issues
- [ WARN] 

# Troubleshooting
### Common Errors
```  ```
Check the connection to the device and ensure it is properly powered.

```  ```
Ensure that the correct serial port is specified and the device is properly connected.

If you can't run any file when you ``` ```  you need to use this code to make your path for ROS 

```

```
# Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes.

# Prerequisites
## Software
- Ubuntu 18.04
- ROS Melodic
- Python 2.7 and Python 3
- arduino IDE
- [MoveIt]
- Git
## Hardware



# Clone the Repository
```

```



# Future
Now I'm developing ROS2 with functions that are more suitable for use in real environments, such as on AMR robots.
