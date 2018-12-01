import cv2
import sys
sys.setrecursionlimit(5000)
video=cv2.VideoCapture(1)
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
    return
t,frame=video.read()
cv2.imshow('Capturing',frame)
cv2.waitKey(0)
if t:
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray,5)
thresh=gray>150
m=thresh & False
for x in range(len(thresh)):
    for y in range(len(thresh[0])):
        if thresh[x][y]:
                #gray[x][y]=255
                thresh[x][y]=255
        else:
                #gray[x][y]=0
                thresh[x][y]=0
cv2.imshow('Capturing',gray)
cv2.waitKey(0)
a=[[]]
for x in range(len(thresh)):
    for y in range(len(thresh[x])):
        if thresh[x][y]==0 and m[x][y]==False:
            high=x
            low=x
            right=y
            left=y
            try:
                floodfill(thresh,x,y,m)
                ch=gray[high:low,left:right]
                a.append([high,low,left,right])
                #ch=cv2.resize(ch,(50,50))
                #cv2.imshow('skdjkjlas',ch)
                #cv2.waitKey(0)
                #a.append(ch)
            except:
                pass
print(a[0][2])
sorted(a,key=lambda x:x[2])
video.release()
cv2.destroyAllWindows