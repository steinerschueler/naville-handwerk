import cv2, numpy as np
img = cv2.imread("multitinker.jpg"); H,W = img.shape[:2]
ov = img.copy()
def L(p,q,c=(255,255,0),t=4): cv2.line(ov,p,q,c,t)
def N(p,name,c=(0,0,255)):
    cv2.circle(ov,p,7,c,-1); cv2.putText(ov,name,(p[0]+6,p[1]-6),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

RW=(328,524); FW=(1130,530); rW=160; ground=685
BB=(700,505); HT=(958,258); HTb=(982,320); ST=(560,300)
stem=(992,40); saddle=(545,95)
tailTop=(120,318); tailBot=(150,552)

for c,r in [(RW,rW),(FW,rW)]:
    cv2.circle(ov,c,r,(255,120,0),3); cv2.circle(ov,c,5,(255,120,0),-1)
cv2.line(ov,(0,ground),(W,ground),(255,0,255),1)

# Rahmen
L(BB,HT,(0,220,0),8)          # Unterrohr/Akku
L(BB,ST,(0,220,0),6)          # Sattelrohr
L(HT,HTb,(0,220,0),6)         # Steuerrohr
L(HTb,FW,(20,20,20),6)        # Gabel
L(HT,stem,(20,20,20),6)       # Lenker/Vorbau
L(ST,saddle,(20,20,20),6)     # Sattelstuetze
# Longtail
L(ST,(500,305),(0,220,0),5); L((500,305),tailTop,(0,220,0),5)  # Deck-Linie
L(BB,tailBot,(0,220,0),6)     # unteres Laengsrohr
L(BB,RW,(0,220,0),5)          # Kettenstrebe
L(tailTop,tailBot,(0,220,0),5)# Heck-Vertikale
L(RW,(tailTop[0],RW[1]),(0,220,0),3)
for p,n in [(BB,"BB"),(HT,"HT"),(HTb,"HTb"),(ST,"ST"),(RW,"RW"),(FW,"FW")]: N(p,n)
cv2.imwrite("skel_overlay.png", ov); print("skel ok")
