import tensorflow as tf
import cv2
import numpy as np
import time

# import sys
# sys.path.append("..")
from drone import *


# All the categories you want your neural network to detect
CATEGORIES = ["Back", "Down", "Forward", "Left", "Right", "Up"]
w, h = 480, 360  # width and height of video
duration1 = 90  # Duration to track green frame
# duration2 = 30

myDrone = intializeTello() # Initialize and connect to drone
myDrone.takeoff() # Send take off command to drone
time.sleep(2) # Wait in 2 second
t1 = time.time() # Get current time
# while(1):
num_black = 0  # Number of black screen

move_forward = 0 # Move forward if black screen in mask

while 1:
    # Take each frame
    frame = telloGetFrame(myDrone, w, h)

    nCols = w
    nRows = h

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # green = np.uint8([[[0, 255, 0]]])  # here insert the bgr values which you want to convert to hsv
    # hsvGreen = cv2.cvtColor(green, cv2.COLOR_BGR2HSV)
    # print(hsvGreen)

    lower_green = np.array([60, 50, 50])
    upper_green = np.array([80, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    cv2.imshow('frame', frame)  # Open original video
    cv2.imshow('mask', mask)  # Open black and white video

    num_point_green = 2000

    # gray_mask = cv2.imread(mask, cv2.IMREAD_GRAYSCALE)
    forward, black = trackGreenFrame_CNN(myDrone, mask, num_point_green)  # Call function to track green frame by CNN model
    num_black += black  # Number of black screen on "mask" (black and white) video

    # If drone does not see green frame any more, it should move forward to pass through the hole of frame
    if num_black > 1:
        move_forward = 1
        break

    # Press "q" if some errors of drone occur to land the drone
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        height = myDrone.get_height()
        print("Height2:", height)
        myDrone.land()
        break

time.sleep(2) # Wait in 2 second
# Move forward after drone in the middle of frame (does not see green color anymore)
if move_forward == 1:
    time.sleep(2)
    myDrone.move_forward(60)

time.sleep(2) # Wait in 2 second
# num_move_forward = 0
num_move_horizontal = 0  # Number of horizontal movements after see red (or blue) spot
num_move_vertical = 0  # Number of vertical movements after see red (or blue) spot
t2 = time.time()

# To check after green frame is red or blue spot
red_detect = 0
blue_detect = 0

while (1):
    frame = telloGetFrame(myDrone, w, h)

    nCols = w
    nRows = h

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # blue = np.uint8([[[255, 0, 0]]])  # here insert the bgr values which you want to convert to hsv
    # hsvBlue = cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
    # print(hsvRed)

    # Range for blue
    blue_lower = np.array([100, 150, 0], np.uint8)
    blue_upper = np.array([140, 255, 255], np.uint8)

    mask = cv2.inRange(hsv, blue_lower, blue_upper)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    point_blue = np.nonzero(mask)  # Get all coordinates of blue spot in video
    row = point_blue[0]  # Get all rows of point_blue
    col = point_blue[1]  # Get all columns of point_blue
    num_point_blue = np.size(point_blue) # Calculate number of blue pixels in video (size of blue spot)
    print("Size of blue point: ", num_point_blue)

    # Get the center coordinate of blue spot in image
    XblueCenter = np.around(np.mean(row))
    YblueCenter = np.around(np.mean(col))
    # Calculate the distance between blue spot to middle row and middle column
    rowOffset = (nRows / 2) - XblueCenter
    colOffset = (nCols / 2) - YblueCenter

    # if num_move > 6:
    #     myDrone.land()
    #     break

    if num_point_blue < 10:  # If drone cannot detect the blue spot, stop to track blue spot and continue to detect red spot
        print('Cannot detect blue object or object is outside')
        myDrone.move_forward(20)
        # myDrone.land()
        break
    else:  # If drone can detect blue spot
        blue_detect = 1  # Set blue_detect = 1 and don't detect red spot (because already detected blue spot)

        # Move drone to make sure blue spot in the center of video
        if num_move_horizontal == 0:
            if colOffset > 50:
                myDrone.move_left(20)
                num_move_horizontal = 1
            elif colOffset < -50:
                myDrone.move_right(20)
                num_move_horizontal = 1
        if num_move_vertical == 0:
            if rowOffset > 50:
                myDrone.move_up(20)
                num_move_vertical = 1
            elif rowOffset < -50:
                myDrone.move_down(20)
                num_move_vertical = 1

        if num_point_blue > 400:  # If blue spot is big enough in video, drone turns left 1m and then lands
            myDrone.rotate_clockwise(90)
            time.sleep(2)
            myDrone.move_forward(100)
            time.sleep(2)
            myDrone.land()
        else: # If blue spot is so small in video, move forward
            myDrone.move_forward(20)
            time.sleep(2)
            # num_move_forward += 1
            # print("num move: ", num_move_forward)

    # Press "q" if some errors of drone occur to land the drone
    if cv2.waitKey(1) & 0xFF == ord('q'):
        height = myDrone.get_height()
        print("Height2:", height)
        myDrone.land()
        break

# If drone did not detect blue spot, try to detect red spot
if blue_detect == 0:
    while(1):
        # Take each frame
        frame = telloGetFrame(myDrone, w, h)

        nCols = w
        nRows = h

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # red = np.uint8([[[0, 0, 255]]])  # here insert the bgr values which you want to convert to hsv
        # hsvRed = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
        # print(hsvRed)

        # Range for lower red
        lower_red = np.array([0, 120, 50])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        # Range for upper range
        lower_red = np.array([170, 100, 50])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)

        # Generating the final mask to detect red color
        mask = mask1 + mask2

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)

        # FROM HERE, SAME IDEA TO DETECT BLUE SPOT
        point_red = np.nonzero(mask)
        row = point_red[0]
        col = point_red[1]
        num_point_red = np.size(point_red)
        print("Size of red point: ", num_point_red)

        XredCenter = np.around(np.mean(row))
        YredCenter = np.around(np.mean(col))
        rowOffset = (nRows / 2) - XredCenter
        colOffset = (nCols / 2) - YredCenter

        # if num_move_forward > 6:
        #     myDrone.land()
        #     print("Move forward many times!")
        #     break

        if num_point_red < 10:
            print('Cannot detect red object or object is outside')
            myDrone.move_forward(20)
            myDrone.land()
            break
        else:
            red_detect = 1
            if num_move_horizontal == 0:
                if colOffset > 50:
                    myDrone.move_left(20)
                    num_move_horizontal = 1
                elif colOffset < -50:
                    myDrone.move_right(20)
                    num_move_horizontal = 1

            if num_move_vertical == 0:
                if rowOffset > 50:
                    myDrone.move_up(20)
                    num_move_vertical = 1
                elif rowOffset < -50:
                    myDrone.move_down(20)
                    num_move_vertical = 1

            if num_point_red > 400:
                myDrone.rotate_counter_clockwise(90)
                time.sleep(3)
                myDrone.move_forward(100)
                time.sleep(3)
                myDrone.land()
            else:
                myDrone.move_forward(20)
                time.sleep(2)
                # num_move_forward += 1
                # print("num move forward: ", num_move_forward)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            height = myDrone.get_height()
            print("Height2:", height)
            myDrone.land()
            break

# If drone cannot detect blue or red spot, drone lands
if blue_detect == 0:
    myDrone.land()

cv2.destroyAllWindows()  # Close all video windows
# if move_forward == 1:
#     time.sleep(2)
#     myDrone.move_forward(100)

# time.sleep(2)
# myDrone.land() # Land the drone






