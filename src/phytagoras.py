import cv2 as cv

def main():
    pObject_mask = "object_mask.jpg"
    pHead_mask = "head_mask.jpg"
    pObject_segmentation = "object_segmentation.jpg"

    object_mask = cv.imread(pObject_mask)
    head_mask = cv.imread(pHead_mask)
    segmentation = cv.imread(pObject_segmentation)

    Object = cv.bitwise_and(segmentation, object_mask)

    cv.imshow("head", head_mask)
    cv.imshow("object", object_mask)
    cv.imshow("object segmentation", segmentation)
    cv.imshow("binary and", Object)
    key = cv.waitKey()

    if key == ord('c'):
        exit()

if __name__ == "__main__":
    main()