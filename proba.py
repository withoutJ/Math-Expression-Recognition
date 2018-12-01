import cv2
import sys

sys.setrecursionlimit(5000)

video=cv2.VideoCapture(0)
high=0
low=0
left=0
right=0
def floodfill(matrix,x,y,m):
    global high
    global low
    global left
    global right
    if x+1<len(matrix):
        if matrix[x+1][y]==0 and m[x+1][y]==False:
            m[x+1][y]=True
            low=max(low,x+1)
            floodfill(matrix,x+1,y,m)
    if x>0:
        if matrix[x-1][y]==0 and m[x-1][y]==False:
            m[x-1][y]=True
            high=min(high,x-1)
            floodfill(matrix,x-1,y,m)
    if y+1<len(matrix[0]):
        if matrix[x][y+1]==0 and m[x][y+1]==False:
            m[x][y+1]=True
            right=max(right,y+1)
            floodfill(matrix,x,y+1,m)
    if y>0:
        if matrix[x][y-1]==0 and m[x][y-1]==False:
            m[x][y-1]=True
            left=min(left,y-1)
            floodfill(matrix,x,y-1,m)
t,frame=video.read()
if t:
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
cv2.imshow('Capturing',gray)
cv2.waitKey(0)
gray = cv2.medianBlur(gray,5)
thresh=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
lmao=gray
w=thresh & False
'''for x in range(len(thresh)):
    for y in range(len(thresh[0])):
        if thresh[x][y]:
                thresh[x][y]=255
                lmao[x][y]=255
        else:
                thresh[x][y]=0
                lmao[x][y]=0'''
gray=gray[70:410,:]
thresh=thresh[70:410,:]
cv2.imshow('Capturing',thresh)
cv2.waitKey(0)
a=[]
for x in range(len(thresh)):
    for y in range(len(thresh[x])):
        if thresh[x][y]==0 and w[x][y]==False:
            high=x
            low=x
            right=y
            left=y
            try:
                floodfill(thresh,x,y,w)
                #ch=gray[high:low,left:right]
                if low-high>10:
                    a.append([high,low,left,right])
                '''ch=cv2.resize(ch,(50,50))
                cv2.imshow('skdjkjlas',ch)
                cv2.waitKey(0)'''
            except:
                pass
a=sorted(a,key=lambda x:x[2])
print(a)
cv2.cv2.destroyAllWindows()  