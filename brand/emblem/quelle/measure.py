import cv2, numpy as np
img = cv2.imread("multitinker.jpg")
H, W = img.shape[:2]
print(f"Bildgroesse: {W}x{H}")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# --- Rote Rahmen-Maske ---
r1 = cv2.inRange(hsv, (0,90,60), (12,255,255))
r2 = cv2.inRange(hsv, (168,90,60), (180,255,255))
red = cv2.bitwise_or(r1,r2)
red = cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
ys,xs = np.where(red>0)
print(f"ROT-Rahmen bbox: x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]  (Breite {xs.max()-xs.min()}, Hoehe {ys.max()-ys.min()})")

# --- Dunkle Maske (Reifen/Anbauten) ---
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
dark = cv2.inRange(gray, 0, 70)
# Hough auf die untere Bildhaelfte fuer die zwei Raeder
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=W*0.25,
                           param1=120, param2=60, minRadius=int(W*0.10), maxRadius=int(W*0.20))
if circles is not None:
    c = np.uint16(np.around(circles))[0]
    c = sorted(c, key=lambda z:z[0])
    for i,(cx,cy,rr) in enumerate(c):
        print(f"Rad {i}: Mitte=({cx},{cy}) r={rr}")
    if len(c)>=2:
        wb = int(c[-1][0])-int(c[0][0])
        print(f"Radstand (Mitte-Mitte): {wb} px = {wb/W:.3f}*Breite")
else:
    print("Keine Kreise gefunden — param2 senken")
