# Robotic_arm_object_tracker
#Created by Sotiris Barlakas- Nikos Iordanidis
The code for our scrap made robotic arm, with OpenCV object detection and tracking, inverse kinematics calculations in MATLAB and ARDUINO code.

![alt text](https://github.com/sotosbarl/Robotic_arm_classifier/blob/main/robotic_arm.png)

By using 2 smartphone cameras in a measured stereo setup we are able to calculate the position of the object (ball) in respect to the camera's coordinate frame.
More specifically, the ball is firstly detected (2d coordinates) in each camera frame using Python's OpenCV. Then by using stereo camera theory (after we have calibrated both cameras) we obtain ball's 3d position:
![image](https://user-images.githubusercontent.com/57687239/178118958-7db67451-61b0-4c04-b831-62596bfb4059.png)

We then transform this position to the robot's base coordinate frame. The "target" position is then sent to our Matlab function, where the appropriate arm's angles are calculated in order for the arm's grip to move to the "target" position. This procedure is generally called inverse kinematics. 

Finally, the appropriate angles are sent to arduino with Serial Communication and are executed by our hardware.
![alt text](https://github.com/sotosbarl/Robotic_arm_classifier/blob/main/Project%20Workflow.png)

See the robot in action: 
https://www.youtube.com/shorts/ZK7stLYL8bI
