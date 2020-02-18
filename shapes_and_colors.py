from pyimagesearch.shapedetector import ShapeDetector
import cv2
import imutils


def color_overlay(mask,image,color):
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
        cv2.putText(image, text, (cX-20, cY),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

def shape_overlay(image):
    resized = imutils.resize(image, width=600)
    ratio = image.shape[0] / float(resized.shape[0])

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sd = ShapeDetector()

    # loop over the contours
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX-20, cY+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

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

shape_overlay(image)

color_overlay(Green,image,'green')
color_overlay(Red,image,'red')
color_overlay(Red2,image,'red')
color_overlay(Blue,image,'blue')

cv2.imshow("Image", image)
cv2.waitKey(27)