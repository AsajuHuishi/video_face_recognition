# -*- coding: utf-8 -*-
import numpy as np
import os
import numpy as np  
import cv2  
import face_recognition
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import threading

global skip_entry
global speed_entry
##旋转图像
def rotate_bound(image,angle):
    #获取图像的尺寸
    #旋转中心
    (h,w) = image.shape[:2]
    (cx,cy) = (w/2,h/2)
    
    #设置旋转矩阵
    M = cv2.getRotationMatrix2D((cx,cy),-angle,1.0)
    cos = np.abs(M[0,0])
    sin = np.abs(M[0,1])
    
    # 计算图像旋转后的新边界
    nW = int((h*sin)+(w*cos))
    nH = int((h*cos)+(w*sin))
    
    # 调整旋转矩阵的移动距离（t_{x}, t_{y}）
    M[0,2] += (nW/2) - cx
    M[1,2] += (nH/2) - cy
    
    return cv2.warpAffine(image,M,(nW,nH))

class video_face_recognition():
    def __init__(self):
        super(video_face_recognition,self).__init__()
        global filename
        self.skip = int(skip_entry.get()) #保存帧间隔数
        self.start = int(start_entry.get()) #从第几帧开始读取
        self.rotate = 1 if v.get() else 0
        self.resize = 1 if v2.get() else 0
        
        self.filename = filename  ##视频名        
        self.cap = cv2.VideoCapture(self.filename)  ##读取视频
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)  ##读取fps每秒传输帧数
        self.total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))#读取视频时长（帧总数）
        (self.name,self.fmt) = os.path.splitext(self.filename) #名称，后缀        
        
        assert self.start < self.total, 'Frametostart is set to large.'
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.start)   #设定从视频的第几帧开始读取   
        print(self.start)
        self.cnt = self.start
        
        self.run()
   
    def run(self):
        while True:
            if self.cnt%10==0:
                print(self.cnt)
            self.cnt+=1
            ret, frame = self.cap.read()#frame(720, 1280, 3)BGR            
            if not ret:##视频读取结束,退出
                break
        
            ## 旋转图片，否则是横过来的
            if self.rotate == 1:
                frame = rotate_bound(frame,90)
            
            if self.resize == 1:
                ## 缩放
                frame = cv2.resize(frame, (1200, 800))
            ## BGR到RGB
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            ## 找到脸的位置
            face_locations = face_recognition.face_locations(frame)
            ## 用蓝色框标记出来
            for (top,right,bottom,left) in face_locations:
                frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # 再转化为BGR,为了cv2显示
            img = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        
            #计算当前时间进度
            now_seconds=int(self.cnt/self.fps%60)
            now_minutes=int(self.cnt/self.fps/60)
            total_second=int(self.total /self.fps%60)
            total_minutes=int(self.total/self.fps/60)
            #   { <参数序号> : <填充> <对齐）> <宽度> <,> <.精度> <类型>}.
            time_now_vs_total="Time:{:>3}:{:>02}|{:>3}:{:0>2}".format(now_minutes,now_seconds,total_minutes,total_second)
            # 输出到画面上
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, time_now_vs_total, (10, 50), font, 1.0, (255, 255, 255), 1)
             
            ## 按帧间隔保存
            if self.skip!=0: 
                if not os.path.isdir(self.name):
                    os.mkdir(self.name)                       
                if self.cnt%self.skip==0:
                    a = self.cnt//self.skip
                    cv2.imwrite(self.name+'/'+str(a)+'.png',img)                
            ## 显示
            cv2.imshow('Video',img)       
            ##按q退出显示
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break        
            ##按空格暂停
            key = cv2.waitKey(1) & 0xff
            if key == ord(' '):
                cv2.waitKey(0)
                
        self.cap.release()
        cv2.destroyAllWindows()
        

#class GUI():
#    def __init__(self):
#        super(GUI,self).__init__()
        
# 多线程解决假死问题
def thread():
    th = threading.Thread(target=video_face_recognition)
    th.setDaemon(True)
    th.start()

## 文件路径
def selectpath():
    global filename
    filename = tkinter.filedialog.askopenfilename()
    file = os.path.basename(filename)
    Label(root,text = file,width = 10).grid(row = 0,column = 1)

    
## 帮助信息
def helpful():
    tkinter.messagebox.askokcancel('提示信息','1、首先点击选择视频文件\n2、保存帧间隔为每隔多少帧保存一次图片,为0时不保存')  
               

root = Tk()
root.geometry('250x180+200+200')
root.title('视频人脸识别 1.0')
Label(root,text = '当前播放:').grid(row = 0,sticky = W)
Button(root,text = '选择视频文件',command = selectpath).grid(row = 2,column = 0,sticky = W)
Label(root,text = '保存帧间隔').grid(row = 3,column = 0) 
skip_entry = Entry(root)
skip_entry['width'] = 10
skip_entry.insert(0,10) ##每10次保存一张图像
skip_entry.grid(row = 3,column = 1)
 
Label(root,text = '从第几帧读取').grid(row = 4,column = 0) 
start_entry = Entry(root)
start_entry['width'] = 10
start_entry.insert(0,1) ##每10次保存一张图像
start_entry.grid(row = 4,column = 1)

v = IntVar()
v.set(1)
Checkbutton(root,text = '翻转',variable = v,onvalue=1,offvalue=0).grid(row = 5,column = 0) 

v2 = IntVar()
v2.set(1)
Checkbutton(root,text = '需要缩放尺寸',variable = v2,onvalue=1,offvalue=0).grid(row = 5,column = 1) 
   
Button(root,text = '帮助',background = 'yellow',command = helpful).grid(row = 2,column = 1,sticky = E)
Button(root,text = '播放',background = 'red',command = thread).grid(row = 2,column = 1,sticky = W)
Label(root,text = '按q退出当前视频').grid(row = 6,column = 0,sticky = W)
Label(root,text = '按空格暂停').grid(row = 6,column = 1,sticky = W)

root.mainloop()
   


