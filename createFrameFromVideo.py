import cv2

video_name = "parking_video2.mp4"
cap = cv2.VideoCapture(video_name)
suc, image = cap.read()
cv2.imwrite("frame0.jpg", image)
