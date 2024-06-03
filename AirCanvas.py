import numpy as np
import cv2
from collections import deque

def setValues(x):
   print("")

#trackbars
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 135, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 205, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 85, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 111, 255,setValues)

#deques to store the coordinates where a line is drawn
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

#indices to access their respective deques
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

#5x5 matrix filled with 1s used for mrphological operations
kernel = np.ones((5,5),np.uint8)

#defining inks for drawing; uses BGR model
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

#defining workspace where drawing can be seen
paintWindow = np.zeros((471,636,3)) + 255

#defining boxes for options in the workspace
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)

#defining text to be filled in the options added
cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

#camera initialization
cap = cv2.VideoCapture(0)

while True:
    #stores frame captured
    ret, frame = cap.read()
  
    #flips the frame
    frame = cv2.flip(frame, 1)
    #converts the colour model from BGR to HSV (to simplify color-based object detectio)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #gets the current positions of trackbars
    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])

    #creating the boxes in the workspace
    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)

    #adding the text in the boxes
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    #operations used to create a well-defined mask of the specified color range
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    #returns a list of contours found in the input image
    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None

    #if contours are detected
    if len(cnts) > 0:
    	#selects the biggest contour
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]        
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        #calculates the moments of the contour
        M = cv2.moments(cnt)
        #computes the centroid of the contour using the moments
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        #checking if the y-coordinate centroid is in the top part where the options are kept
        if center[1] <= 65:
            #if present in the area of the clear option
            if 40 <= center[0] <= 140: 
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                #indices to access their respective deques
                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                #setting the whole workspace from index 67 onwards to white
                paintWindow[67:,:,:] = 255
            #checking if the centroid lies in the regin of the
            #colour options and changing colour accordingly
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 
        #if the centroid is in the portion below the options
        else :
            if colorIndex == 0:
                #centroid is stored in the deque of that respective colour
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
    #if there are not contours
    else:
        #new deque is added for each stroke of a colour when 
        #a contour isn't detected i.e. pen isn't detected
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    #draws a line between the points recorded in the deque of each colour
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    #displaying all the windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    cv2.imshow("mask",Mask)

    #exits the program when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

#ends the project by releasing the camera and closing all the windows
cap.release()
cv2.destroyAllWindows()
