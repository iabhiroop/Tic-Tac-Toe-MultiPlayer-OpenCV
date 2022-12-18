import cv2
import numpy as np

# Create Mask Variable
def mask_contour():
    Upper_hsv = np.array([255,255,255])
    Lower_hsv = np.array([59,128,0])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((5,5),np.uint8)
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)
    return Mask

# Method to find Center of Pointer
def find_center():
    global Mask
    Mask=mask_contour()
    cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None
    if len(cnts) > 0:
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        M = cv2.moments(cnt)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
    return center

# Locate the Spatial Position  of Pointer
def spacial_location_check(center):
    global x,xo
    for i in range(3):
        for j in range(3):
            if m2d[i,j]==-1 and center[0] in range(bxs[j,i,0],bxl[j,i,0]) and center[1] in range(bxs[j,i,1],bxl[j,i,1]):
                x.append([i,j])
                if x[0]!=x[-1]:
                    x=[]
                elif len(x)==20:
                    m2d[i,j]=xo
                    xo=(xo+1)%2

# Keep track and check score of the game
def win_check(frame):
    wi=['X','O']
    if len(set(np.diag(m2d)))==1 and m2d[0,0]!=-1:
        frame = cv2.putText(frame,wi[m2d[0,0]]+' wins',(si,si//3),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 128), 2, cv2.LINE_AA)
        return 1
    elif len(set(np.fliplr(m2d).diagonal()))==1 and m2d[0,2]!=-1:
        frame = cv2.putText(frame,wi[m2d[2,2]]+' wins',(si,si//3),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 128), 2, cv2.LINE_AA)
        return 1
    else:
        for i in range(3):
            if m2d[i,0]==m2d[i,1]==m2d[i,2]!=-1:
                frame=cv2.putText(frame,wi[m2d[i,1]]+' wins',(si,si//3),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 128), 2, cv2.LINE_AA)
                return 1
            elif m2d[0,i]==m2d[1,i]==m2d[2,i]!=-1:
                frame=cv2.putText(frame,wi[m2d[0,i]]+' wins',(si,si//3),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 128), 2, cv2.LINE_AA)
                return 1
    if center!=None:
            spacial_location_check(center)
    return 0

# Create graphics on frame to split tic-tac=toe table and split frame into pieces
def xo_graphics():
    global m2d,x
    for i in range(4):
        cv2.line(frame,((si//3)*i,0),((si//3)*i,si),(255, 0, 128),2)
        cv2.line(frame,(0,(si//3)*i),(si,(si//3)*i),(255, 0, 128),2)
    for i in range(3):
        for j in range(3):
            k=m2d[i][j]
            if k in [0,1]:
                frame[bl[i]:bl[i+1],bl[j]:bl[j+1]]=imgl[k]
    y=win_check(frame)
    if y==1 and center !=None and  center[0] in range(si+5,si+200):
        x.append('r')
        if x[0]!=x[-1]:
            x=[]
        elif len(x)==25:
            m2d=np.full((3,3),-1)

            
if __name__ == '__main__':
    m2d=np.full((3,3),-1)
    bxs=np.full((3,3,2),0)
    bxl=np.full((3,3,2),0)
    si=600
    bl=[0,si//3,(si//3)*2,si]
    for i in range(3):
        for j in range(3):
            bxs[i,j]=(bl[i],bl[j])
            bxl[i,j]=(bl[i+1],bl[j+1])
    
    # Load X and O Images and resize to fit into frame pieces
    imgx = cv2.imread(r'x.png')
    imgo = cv2.imread(r'o.png')
    imgx = cv2.resize(imgx,(int(si//3),int(si//3)), fx = 0.1, fy = 0.1)
    imgo = cv2.resize(imgo,(int(si//3),int(si//3)), fx = 0.1, fy = 0.1)
    imgl=[imgx,imgo]
    xo=0
    x=[]
    
    # Video Capture
    cap = cv2.VideoCapture(0)
    
    # Let's Play Tic-Tac-Toe !!!
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame,(si+200,si), fx = 0.1, fy = 0.1)
        if(ret):
            center=find_center()
            xo_graphics()
            cv2.imshow("output", frame)
            if (cv2.waitKey(1) & 0xFF == ord('q')):
                break
        else:
            break
    cv2.destroyAllWindows()
    cap.release()
