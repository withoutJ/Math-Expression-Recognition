import numpy as np
import tensorflow as tf 
from tensorflow import keras
import cv2
import keyboard
import sys
from operator import itemgetter
sys.setrecursionlimit(5000)
txt=open("data_base.txt","r")
a=txt.read()
a=a.split("\n")
a=a[:-1]
#upisi iz baze train slike u niz
pom=[[[]]]
for x in a:
    b=x.split(";")
    m=[]
    for i in b:
        m.append(i.split(",")[:-1])
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j]!="":
                m[i][j]=int(m[i][j])
    m=m[:-1]
    pom.append(m)
pom=pom[1:]
train_images=np.zeros((4200,50,50))
for p in range(4200):
    for q in range(50):
        for r in range(50):
            train_images[p][q][r]=pom[p][q][r]
#upisi train labele u niz
pom1=[]
x=0
for i in range(14):
    for j in range(300):
        pom1.append(x)
    x+=1
train_labels=np.array(pom1)
#upisi iz txt test slike u niz
txt=open("test_base.txt","r")
a=txt.read()
a=a.split("\n")
a=a[:-1]
pom=[[[]]]
for x in a:
    b=x.split(";")
    m=[]
    for i in b:
        m.append(i.split(",")[:-1])
    for i in range(len(m)):
        for j in range(len(m[i])):
            m[i][j]=int(m[i][j])
    m=m[:-1]
    pom.append(m)
pom=pom[1:]
test_images=np.zeros((140,50,50))
for p in range(140):
    for q in range(50):
        for r in range(50):
            test_images[p][q][r]=pom[p][q][r]
#upisi test labele u niz
pom1=[]
x=0
for i in range(14):
    for j in range(10):
        pom1.append(x)
    x+=1
test_labels=np.array(pom1)
#neuroni su od 0 do 1
for p in range(len(train_images)):
    for q in range(len(train_images[p])):
            for r in range(len(train_images[p][q])):
                    train_images[p][q][r]=train_images[p][q][r]/255.0
for p in range(len(test_images)):
    for q in range(len(test_images[p])):
        for r in range(len(test_images[p][q])):
            test_images[p][q][r]=test_images[p][q][r]/255.0

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(50, 50)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(14, activation=tf.nn.softmax)
])

model.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=5)

test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)


while True:
    try:
        if keyboard.is_pressed('c'):
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
            w=thresh & False
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
                            #ch=cv2.resize(ch,(50,50))
                            #cv2.imshow('skdjkjlas',ch)
                            #cv2.waitKey(0)
                        except:
                            pass
            a=sorted(a,key=lambda x:x[2])
            #print(a)
            pics_exp=[]
            for k in a:
                high=k[0]
                low=k[1]
                left=k[2]
                right=k[3]
                ch=gray[high:low,left:right]
                ch=cv2.resize(ch,(50,50))
                pics_exp.append(ch)
            gej=np.zeros((len(pics_exp),50,50))
            for i in range(len(pics_exp)):
                    for j in range(len(pics_exp[i])):
                        for r in range(len(pics_exp[i][j])):
                            gej[i][j][r]=pics_exp[i][j][r]/255.0
            predictions=model.predict(gej)
            exp=[]
            for p in predictions:
                exp.append(np.argmax(p))
            #print(exp)
            mxp=''
            for i in exp:
                if i==10:
                    mxp=mxp+'+'
                elif i==11:
                    mxp=mxp+'-'
                elif i==12:
                    mxp=mxp+'*'
                elif i==13:
                    mxp=mxp+'/'
                else:
                    mxp=mxp+str(i)
            print(mxp)
            try:
                solution=eval(mxp)
                print(solution)
            except:
                pass
            break
        else:
            pass
    except:
        print('jsakdjsk')
        break  
cv2.destroyAllWindows()