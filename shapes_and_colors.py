import cv2
import imutils


def filter(mask,image,color):
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]) )
        c = c.astype("float")
        c = c.astype("int")
        text = "{}".format(color)
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, text, (cX, cY),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


greenLower = (50, 100, 100)
greenUpper = (80, 255, 255)
redLower = (0, 100, 100)
redUpper = (49, 255, 255)
blueLower = (81, 100, 100)
blueUpper = (120, 255, 255)
redLower2 = (140, 100, 100)
redUpper2 = (180, 255, 255)


image = cv2.imread('shapes_and_colors.png')
blurred = cv2.GaussianBlur(image, (11, 11), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

Green = cv2.inRange(hsv, greenLower, greenUpper)
Red = cv2.inRange(hsv, redLower, redUpper)
Red2 = cv2.inRange(hsv, redLower2, redUpper2)
Blue = cv2.inRange(hsv, blueLower, blueUpper)

filter(Green,image,'green')
filter(Red,image,'red')
filter(Red2,image,'red')
filter(Blue,image,'blue')

cv2.imshow("Image", image)
cv2.waitKey(0)