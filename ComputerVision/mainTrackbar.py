import cv2
import numpy as np

def nothing(x):
    pass

# creat trackbar in windows
img = np.zeros((255, 255 ,3), np.uint8)
cv2.namedWindow('imgBar')

# creat trackbars for color change
cv2.createTrackbar('B', 'imgBar', 0, 255, nothing)
cv2.createTrackbar('G', 'imgBar', 0, 255, nothing)
cv2.createTrackbar('R', 'imgBar', 0, 255, nothing)
# switch on & off
switch = '0: OFF \n 1: ON'
cv2.createTrackbar(switch, 'imgBar', 0, 1, nothing)

while True:
    cv2.imshow('imge', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    # get BGR value for trackbar
    s = cv2.getTrackbarPos(switch, 'imgBar')
    b = cv2.getTrackbarPos('B', 'imgBar')
    g = cv2.getTrackbarPos('G', 'imgBar')
    r = cv2.getTrackbarPos('R', 'imgBar')

    if s == 0:
        pass
    elif s == 1:
        img[:] = [b, g, r]

cv2.destroyAllWindows()