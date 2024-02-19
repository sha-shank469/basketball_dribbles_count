import cv2
from basketball_tracker import Basketball_tracker
from kalmanfilter import KalmanFilter

cap = cv2.VideoCapture("basket_ball.mp4")

# Load detector
od = Basketball_tracker()

# Load Kalman filter to predict the trajectory
kf = KalmanFilter()

while True:
    ret, frame = cap.read()
    if ret is False:
        break

    orange_bbox = od.detect(frame)
    x, y, x2, y2 = orange_bbox
    cx = int((x + x2) / 2)
    cy = int((y + y2) / 2)

    predicted = kf.predict(cx, cy)
    #cv2.rectangle(frame, (x, y), (x2, y2), (255, 0, 0), 4)
    cv2.circle(frame, (cx, cy), 20, (0, 0, 255), 4)
    cv2.circle(frame, (predicted[0], predicted[1]), 20, (255, 0, 0), 4)

    cv2.namedWindow("Frame",cv2.WINDOW_NORMAL)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(150)
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()