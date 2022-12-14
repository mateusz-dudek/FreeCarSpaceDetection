import cv2
import pickle

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

#Type width and height of the parking spot area
width, height = 145, 70

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread("frame0.jpg")
    img = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA)

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseClick)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break