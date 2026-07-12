import cv2, numpy as np
img = cv2.imread("multitinker.jpg"); gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
def measure(name, x0,x1,y0,y1):
    reg = gray[y0:y1, x0:x1]
    best=None
    for p2 in (75,65,55,45,38):
        c=cv2.HoughCircles(reg,cv2.HOUGH_GRADIENT,dp=1.2,minDist=400,
                           param1=120,param2=p2,minRadius=100,maxRadius=150)
        if c is not None:
            cx,cy,r=c[0][0]; best=(int(cx)+x0,int(cy)+y0,int(r),p2); break
    print(name, best)
    return best
r=measure("REAR", 170,490, 390,690)
f=measure("FRONT", 980,1300, 400,695)
if r and f:
    print("Radstand:", f[0]-r[0], " r_mittel:", (r[2]+f[2])//2, " ground~:", (r[1]+r[2]+f[1]+f[2])//2)
