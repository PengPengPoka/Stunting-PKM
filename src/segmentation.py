import cv2 as cv
import os
import numpy as np

def nothing():
    pass

def main():
    img_path = "C:\\Users\\OMEN\\Repositories\\Stunting - PKM\\Data\\Panjang\\bayi_1.jpg"

    img = cv.imread(img_path)

    if img is None:
        print("image is None")

    img = cv.resize(img, (640,480))
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    hlow = slow = vlow = 0
    hup = sup = vup = 0

    cv.namedWindow("trackbar")
    cv.createTrackbar("hue low", "trackbar", 0, 179, nothing)
    cv.createTrackbar("sat low", "trackbar", 0, 255, nothing)
    cv.createTrackbar("val low", "trackbar", 0, 255, nothing)

    cv.createTrackbar("hue max", "trackbar", 0, 179, nothing)
    cv.createTrackbar("sat max", "trackbar", 0, 255, nothing)
    cv.createTrackbar("val max", "trackbar", 0, 255, nothing)

    while img is not None:
        hlow = cv.getTrackbarPos("hue low", "trackbar")
        slow = cv.getTrackbarPos("sat low", "trackbar")
        vlow = cv.getTrackbarPos("val low", "trackbar")

        hup = cv.getTrackbarPos("hue max", "trackbar")
        sup = cv.getTrackbarPos("sat max", "trackbar")
        vup = cv.getTrackbarPos("val max", "trackbar")

        low = np.array([hlow,slow,vlow])
        uppper = np.array([hup,sup,vup])

        obj_segmentation = cv.inRange(img_hsv,low, uppper)

        cv.imshow("image", img)
        cv.imshow("trackbar", obj_segmentation)
        key = cv.waitKey(3)

        if key == ord('c'):
            # cv.imwrite("object mask.jpg", obj_mask)
            break

if __name__ == "__main__":
    main()