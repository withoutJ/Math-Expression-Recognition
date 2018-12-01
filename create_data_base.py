import cv2
import sys
import numpy as  np
sys.setrecursionlimit(300000)
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

gray=cv2.imread('deljenje.jpg',0)
gray = cv2.medianBlur(gray,5)
thresh=gray>150
m=thresh & False
for x in range(len(thresh)):
    for y in range(len(thresh[x])):
        if thresh[x][y]:
                thresh[x][y]=255
        else:
                thresh[x][y]=0
#cv2.imshow('skdjkjlas',w)
#cv2.waitKey(0)
txt=open("data_base.txt","a")
r=0
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
                ch=cv2.resize(ch,(50,50))
                r+=1
                print(r)
                for i in ch:
                    for j in i:
                        txt.write(str(j))
                        txt.write(",")
                    txt.write(";")
                txt.write("\n")
                #cv2.imshow('skdjkjlas',ch)
                #cv2.waitKey(0)
            except:
                pass

txt.close()
cv2.destroyAllWindows