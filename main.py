import cv2
import pickle
import numpy as np
import cvzone

cap = cv2.VideoCapture("carPark.mp4")

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48


def CheckParkSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop)
        counts = cv2.countNonZero(imgCrop)

        if counts <= 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(counts), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (20, 0 + height - 3), scale=2, thickness=5,
                       offset=20, colorR=(0, 200, 0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_FRAME_COUNT, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThresh, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    CheckParkSpace(imgDilate)

    # for pos in posList:

    cv2.imshow("img", img)
    # cv2.imshow("imgBlur", imgBlur)
    # cv2.imshow("imgThresh", imgThresh)
    cv2.waitKey(10)