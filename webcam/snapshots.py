import cv2
import time


cam = cv2.VideoCapture(0)

n = 0
while n < 1000:
    ret, im = cam.read()
    # cv2.imshow('', im)
    # cv2.waitKey(0)
    cv2.imwrite('/Users/user/python/detectron/webcam/img/' + str(n)+'.jpg', im)
    n += 1
    print(n)
    time.sleep(0.01)