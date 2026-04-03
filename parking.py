import cv2
import pickle

width, height = 107, 48
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseclick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, v in enumerate(posList):
            x1, y1 = v
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    # cv2.rectangle(img,(50,193),(157,240),(255,0,255),2)
    img = cv2.imread('carParkImg.png')

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow('image', img)
    cv2.setMouseCallback("image", mouseclick)
    cv2.waitKey(1)
