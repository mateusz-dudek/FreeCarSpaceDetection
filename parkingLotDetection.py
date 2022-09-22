import cv2
import pickle
import cvzone
import numpy as np

width, height = 145, 70
cap = cv2.VideoCapture("parking_video2.mp4")

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

def checkPArkingSpace(imgProcessed):
    spaceCounter = 0
    for pos in posList:
        x, y = pos
        imgCrop = imgProcessed[y:y+height, x:x+width]
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x + 10, y+height - 10), scale=0.5,
                           thickness=1, offset=0, colorR=(0, 0, 255))

        if count < 1000:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img, f'Free: {spaceCounter} / {len(posList)}', (100, 50), scale=1,
                       thickness=2, offset=5, colorR=(0, 200, 0))

while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    succes, img = cap.read()
    img = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 71, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkPArkingSpace(imgDilate)
    img = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA)
    cv2.imshow("Image", img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break