# Robotic_arm_object_tracker
#Created by Sotiris Barlakas- Nikolaos Iordanidis

## Abstract

Sotiris and Nikolaos embarked on this personal project as an experiment in Computer Vision. It also provided them with an opportunity to apply their expertise in kinetics-dynamics and programming. The core idea behind the project was for the robotic arm to employ Computer Vision to classify two distinct types of objects, white and orange ping pong balls, and accurately position them in their respective designated locations.

## Manufacturing the robotic arm

To construct the robotic arm, aluminum coffee cans were employed. They were cut and shaped into sturdy cuboids, which served as the individual segments of the arm. The base utilized a disc case containing a dozen computer discs to ensure stability. Additionally, the portion of the arm responsible for handling ping pong balls was fashioned from cardboard obtained from boxes, featuring a scoop-like geometry. Servomotors were employed for all rotational movements, spanning from the base to the final segment. 


![alt text](https://github.com/sotosbarl/Robotic_arm_object_tracker/blob/main/robotic_arm.png)


## Computer Vision equipment

By using 2 smartphone cameras in a measured stereo setup we are able to calculate the position of the object (ball) in respect to the camera's coordinate frame.
More specifically, the ball is firstly detected (2d coordinates) in each camera frame using Python's OpenCV. Then by using stereo camera theory (after we have calibrated both cameras) we obtain ball's 3d position:
![image](https://user-images.githubusercontent.com/57687239/178118958-7db67451-61b0-4c04-b831-62596bfb4059.png)

We then transform this position to the robot's base coordinate frame. The "target" position is then sent to our Matlab function, where the appropriate arm's angles are calculated in order for the arm's grip to move to the "target" position. This procedure is generally called inverse kinematics.
Finally, the appropriate angles are sent to arduino with Serial Communication and are executed by our hardware.

## Workflow diagram
![alt text](https://github.com/sotosbarl/Robotic_arm_object_tracker/blob/main/Project%20Workflow.png)

See the robot in action: 
https://www.youtube.com/shorts/ZK7stLYL8bI
