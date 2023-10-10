# This is the code for identifying an object (ball) as well as finding its location (x,y,z)  in 3d space

# Library
import requests
import cv2
import imutils
import matlab.engine
import time
import serial
import numpy as np



# Functions
def coordinates_transformation(x_camera,y_camera,z_camera):
    x_arm = x_camera + Coordinate_system_offset_x
    y_arm = y_camera + Coordinate_system_offset_y
    z_arm = z_camera + Coordinate_system_offset_z
    return x_arm,y_arm,z_arm

def empty():
    pass

def getContours(img,imgContour):
    x=0
    y=0
    cx=0
    cy=0
    flag1=0
    #approx=np.array([1,0,1])
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(imgContour,contours,-1,(225,0,0),7)
    contour_list=[]

    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>5000:
            contour_list.append(cnt)
            #cv2.drawContours(imgContour,cnt,-1,(225,0,255),6)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                flag1=1

            # a=[]
            # b=[]
            #
            # for i in range(0,len(approx)):
            #     a.append(approx[i,0,0])
            #     b.append(approx[i,0,1])
            # x=statistics.mean(a)
            # y=statistics.mean(b)
            # flag1=1
            x = cx
            y = cy


            cv2.drawContours(imgContour,[approx],-1,(225,0,255),6)
    return x, y, flag1



eng = matlab.engine.start_matlab()
arduino = serial.Serial("COM8", 9600, timeout=.1)

time.sleep(1) #give the connection a second to settle

url1 = "http://192.168.1.32:8080/shot.jpg"          #left
url2 = "http://192.168.1.25:8080/shot.jpg"           #right


fx = 3.66371254e+03
fy = 6.70809677e+03
cx = 4.08796856e+02
cy = 3.08194048e+02
b = 200

#cap = cv2.VideoCapture(url1)

Coordinate_system_offset_x=8
Coordinate_system_offset_y=8
Coordinate_system_offset_z=8



cv2.namedWindow ("HSV")
cv2.namedWindow ("parameters")
cv2.resizeWindow('parameters',640,240)
cv2.resizeWindow('HSV',640,240)

cv2.createTrackbar('HUE Min','HSV',0,179,empty)
cv2.createTrackbar('HUE Max','HSV',179,179,empty)
cv2.createTrackbar('SAT Min','HSV',0,255,empty)
cv2.createTrackbar('SAT Max','HSV',255,255,empty)
cv2.createTrackbar('Value Min','HSV',0,255,empty)
cv2.createTrackbar('Value Max','HSV',255,255,empty)

cv2.createTrackbar('threshold1','parameters',0,255,empty)
cv2.createTrackbar('threshold2','parameters',0,255,empty)
approx=0




while True:
    page = ''
    while page == '':
        try:
            page = requests.get(url1)
            break
        except:
            print("Connection refused by the server...")
            print("Give me 5 seconds")
            print("Loading...")
            time.sleep(5)
            print("Ok! Lets continue")
            continue
    img_resp=page
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    frame=cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = imutils.resize(frame, width=1000, height=1800)

    # ret, frame=cap.read()
    #frame = imutils.resize(frame, width=1000, height=1800)

    imgContour=frame.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blur=cv2.GaussianBlur(frame,(7,7),1)
    gray=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)

    #
    # h_min=cv2.getTrackbarPos('HUE Min','HSV')
    # h_max=cv2.getTrackbarPos('HUE Max','HSV')
    # s_min=cv2.getTrackbarPos('SAT Min','HSV')
    # s_max=cv2.getTrackbarPos('SAT Max','HSV')
    # v_min=cv2.getTrackbarPos('Value Min','HSV')
    # v_max=cv2.getTrackbarPos('Value Max','HSV')
    # t1=cv2.getTrackbarPos('threshold1','parameters')
    # t2=cv2.getTrackbarPos('threshold2','parameters')

    # lower=np.array([h_min,s_min,v_min])
    # upper=np.array([h_max,s_max,v_max])
    # lower=np.array([137,149,24])
    # upper=np.array([179,255,255])
    lower = np.array([0, 110, 114])
    upper = np.array([84, 213, 255])
    mask=cv2.inRange(hsv,lower,upper)
    result=cv2.bitwise_and(frame, frame, mask=mask)

    imgcanny=cv2.Canny(mask,1,2)
    kernel=np.ones((5,5))
    imgDil=cv2.dilate(imgcanny,kernel, iterations=1)

    # lower_blue = np.array([90, 150, 150])
    # upper_blue = np.array([100, 255, 255])
    #
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # ret, thresh= cv2.threshold(mask,0,255,0)
    # contours, hierarchy =cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # result = cv2.bitwise_and(frame, frame, mask=mask)

    #cv2.imshow('frame', hsv)
    #cv2.imshow('result', result)
    #cv2.imshow('mask', mask)
    #cv2.imshow('imgDil', imgDil)
    #cv2.imshow('canny', imgcanny)
    x1, y1, flag1 = getContours(imgDil,imgContour)
    cv2.circle(imgContour, (x1, y1), 7, (0, 0, 255), -1)

    cv2.imshow('imgContour', imgContour)
    #print(arduino.readline().decode('utf-8'))
    #print(x)


###################################################################
#                     SECOND CAMERA
    page2 = ''
    while page2 == '':
        try:
            page2 = requests.get(url2)
            break
        except:
            print("Connection refused by the server...")
            print("Give me 5 seconds")
            print("Loading...")
            time.sleep(5)
            print("Ok! Lets continue")
            continue
    img_resp2=page2
    img_arr2 = np.array(bytearray(img_resp2.content), dtype=np.uint8)
    frame2 = cv2.imdecode(img_arr2, -1)
    frame2=cv2.rotate(frame2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame2 = imutils.resize(frame2, width=1000, height=1800)

    # ret, frame=cap.read()
    #frame = imutils.resize(frame, width=1000, height=1800)

    imgContour2=frame2.copy()

    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    blur2=cv2.GaussianBlur(frame2,(7,7),1)
    gray2=cv2.cvtColor(blur2,cv2.COLOR_BGR2GRAY)

    #
    h_min=cv2.getTrackbarPos('HUE Min','HSV')
    h_max=cv2.getTrackbarPos('HUE Max','HSV')
    s_min=cv2.getTrackbarPos('SAT Min','HSV')
    s_max=cv2.getTrackbarPos('SAT Max','HSV')
    v_min=cv2.getTrackbarPos('Value Min','HSV')
    v_max=cv2.getTrackbarPos('Value Max','HSV')
    t1=cv2.getTrackbarPos('threshold1','parameters')
    t2=cv2.getTrackbarPos('threshold2','parameters')

    # lower2=np.array([h_min,s_min,v_min])
    # upper2=np.array([h_max,s_max,v_max])
    # lower2=np.array([0,79,242])
    # upper2=np.array([54,203,255])
    lower2 = np.array([137, 149, 24])
    upper2 = np.array([179, 255, 255])


    mask2=cv2.inRange(hsv2,lower2,upper2)
    result2=cv2.bitwise_and(frame2,frame2,mask=mask2)

    imgcanny2=cv2.Canny(mask2,1,2)
    kernel2=np.ones((5,5))
    imgDil2=cv2.dilate(imgcanny2,kernel2, iterations=1)

    # lower_blue = np.array([90, 150, 150])
    # upper_blue = np.array([100, 255, 255])
    #
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # ret, thresh= cv2.threshold(mask,0,255,0)
    # contours, hierarchy =cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # result = cv2.bitwise_and(frame, frame, mask=mask)

    # cv2.imshow('frame', hsv2)
    # cv2.imshow('result', result2)
    # cv2.imshow('mask', mask2)
    # cv2.imshow('imgDil', imgDil2)
    # cv2.imshow('canny', imgcanny2)



    x2,y2,flag2=getContours(imgDil2,imgContour2)
    cv2.circle(imgContour2, (x2, y2), 7, (0, 0, 255), -1)

    cv2.imshow('imgContour2', imgContour2)

    if flag1 == 0:
        print('Ball not identified by camera1')
    else:
        ul = x1
        vl = y1

    if flag2 == 0:
        print('Ball not identified by camera2')
    else:
        ur = x2
        vr = y2


#if ball is identified in both cameras then, using the stereo setup equations we can calculate ball's position with
# respect to global coordinates frame.
    if flag1 != 0 and flag2 != 0:
        X = b * (ul - cx) / (ul - ur)
        Y = b * fx * (vl - cy) / (fy * (ul - ur))
        Z = -b * fx / (ul - ur)

        depth = 0.01 * Z  # centimetres
        print('y=', 0.1 * Y)
        print('x=', 0.1 * X)
        print('z', depth)

        x_camera = 0.1 * X
        y_camera = 0.1 * Y
        z_camera = 0.01 * Z

        flag = True

        if x_camera > 40:
            flag = False
        if y_camera > 30:
            flag = False
        if z_camera > 50:
            flag = False


        x = x_camera + 20
        y = z_camera - 20
        z = y_camera
        print('y=', y)
        print('x=', x)
        print('z', z)

#Next, we send the ball's coordinates to matlab to calculate (using inverse kinematics) the desired servo angles in
#in order for the arm's end to catch the ball
        out = eng.Robot_catch_me(x, z, 0, 0, 0, nargout=3)

        print('theta', out[0])
        print('phi', out[1])

        if not (sum(out) == 15000) and flag:
            difference_down = int(out[0])-75
            theta = str(1000+170+difference_down)

            difference_up = int(out[1])-90
            phi = str(10000+40-difference_up+difference_down)
            #lamda = str(int(out[2]))
            r = (x**2+y**2)**0.5
            base_angle = np.arcsin(y/r)
            base_angle = np.rad2deg(base_angle)+120
            print('base', base_angle)

            base_angle = str(base_angle)

            arduino.write(bytes(theta, 'utf-8'))
            time.sleep(4)

            #send the calculated desired angles to arduino to move the arm accordingly to catch the ball
            print(arduino.readline(10))
            arduino.write(bytes(phi, 'utf-8'))
            time.sleep(4)
            print(arduino.readline(10))

            arduino.write(bytes(base_angle, 'utf-8'))
            time.sleep(2)
            print(arduino.readline(10))

            time.sleep(4)
            print(arduino.readline(10))
            time.sleep(4)


        else:
            arduino.write(bytes('666', 'utf-8'))
            time.sleep(1)
            arduino.write(bytes('666', 'utf-8'))
            time.sleep(1)
            arduino.write(bytes('666', 'utf-8'))





    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
