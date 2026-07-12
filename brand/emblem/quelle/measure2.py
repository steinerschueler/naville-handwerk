import cv2, numpy as np
img = cv2.imread("multitinker.jpg")
H, W = img.shape[:2]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
r1 = cv2.inRange(hsv, (0,90,60), (12,255,255)); r2 = cv2.inRange(hsv,(168,90,60),(180,255,255))
red = cv2.bitwise_or(r1,r2)
red = cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((4,4),np.uint8))

ov = img.copy()
# rote Maske gruen tinten
ov[red>0] = (0,255,0)
# gemessene Raeder
wheels = [(328,524,161),(1130,530,161)]
for cx,cy,r in wheels:
    cv2.circle(ov,(cx,cy),r,(255,0,0),3); cv2.circle(ov,(cx,cy),4,(255,0,0),-1)
ground = 524+161
cv2.line(ov,(0,ground),(W,ground),(255,0,255),2)
# Raster
for x in range(0,W,50):
    cv2.line(ov,(x,0),(x,H),(200,200,200),1)
    if x%100==0: cv2.putText(ov,str(x),(x+2,18),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,0),1)
for y in range(0,H,50):
    cv2.line(ov,(0,y),(W,y),(200,200,200),1)
    if y%100==0: cv2.putText(ov,str(y),(2,y+16),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,0),1)
cv2.imwrite("mess_overlay.png", ov)
print("overlay ok", W, H, "ground=", ground)
