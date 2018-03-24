import cv2
import numpy as np

# cam0 = cv2.VideoCapture(0)
# cam1 = cv2.VideoCapture(1)

print("Go")
# vcap = cv2.VideoCapture("rtsp://192.168.128.13:554/user=admin_password=tlJwpbo6_channel=1_stream=1.sdp?real_stream")
# vcap = cv2.VideoCapture("rtsp://192.168.128.12:554/mpeg4cif")
vcap = cv2.VideoCapture("rtsp://192.168.128.11:554/av0_1")
while(1):
    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    k = cv2.waitKey(10)
    if k > 0:
        print("Key pressed, closing...")
        break

vcap.release()
cv2.destroyAllWindows()

# img_counter = 1
#
# while True:
#     ret0, img0 = cam0.read()
#     if not ret0:
#         break
#
#     ret1, img1 = cam1.read()
#     if not ret1:
#         break
#
#     s0 = cv2.resize(img0, (480, 270))
#     s1 = cv2.resize(img1, (480, 270))
#
#     vis = np.concatenate((s0, s1), axis=0)
#
#     cv2.imshow('cams', vis)
#
#     print("run")
#
#     k = cv2.waitKey(1)
#
#     print("key")
#
#     if k % 256 == 27:
#         # ESC pressed
#         print("Escape hit, closing...")
#         break
#     elif k % 256 == 32:
#         # SPACE pressed
#         img = np.concatenate((img0, img1), axis=1)
#         img_name = "img_{}.png".format(img_counter)
#         cv2.imwrite(img_name, img)
#         print("{} written!".format(img_name))
#         img_counter += 1

