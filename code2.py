
import cv2 #opencv for image processing
#creating a videocapture object
import time
import numpy as np
## preparing for writing the output video
fourcc = cv2.VideoWriter_fourcc(*'MJPG') ##popular open source video compression tec
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
cap = cv2.VideoCapture(0) #this is my webcam

#wait 2 seconds before the webcom starts
time.sleep(2)
count = 0
background = 0

#capture the background in the range of 60; red == 60 on HUE 
for i in range(60):
    ret, background = cap.read()
background = np.flip(background, axis = 1)

#getting the background image, while the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count += 1
    img = np.flip(img, axis=1)
    
#converting the colour space from BGR to HSV

hsv =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#generating mask to detect red colour HSV(60)

lower_red = np.array(0, 120, 50)
upper_red = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv, lower_red, upper_red)

#opening and dilateting the mask image
mask1 = cv2.morophologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
mask2 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3), np.unit8))

#creating inverted mask to segemnt out the red colour from the web frame
mask2 =cv2.bitwise_not(mask2)

#segment the red colour part out of the frame using bitwise and with the inverted mask
res1 = cv2.bitwise_and(img,img, mask = mask2)

#creating image showing static background frame pixels only for the masked region
res2 = cv2.bitwise_and(background, background, mask = mask1)

#generating the final output and writing 
finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
out.write(finalOutput)
cv2.imshow("magic", finalOutput)
cv2.waitKey(1)

cap.release()
out.release(
cv2.destroyAllWindows())  #will close all the programming window
