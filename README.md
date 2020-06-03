## GUI for Video Face Recognition
It is the code to **generate a GUI for Video Face Recognition** based on Python and Face_recognition library. We generate a graphical interface to input a video, capture and output the human face in the video. It is based on article: [opencv+face_recognition+tkinter: 实现简单的视频人脸识别工具](https:). 

## Requirements
* Python 
* cv2 
* face-recognition [Github](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py)
* tkinter


The technical foundation of this paper is divided into three parts:
|lib  | usage |
|--|--|
| opencv | Video processing module|
| face_recognition | Face recognition module |
| tkinter|GUI design module|

## Results & How to use
Example:
```
python shizuo.py
```

Our window design is as follows:
<div align='center'>
<img src='https://img-blog.csdnimg.cn/20200603002715240.png'>
</div>

GUI function:

* For the vertical video, you need to flip it

* For oversized videos, you need to downsize the display

* For long videos, you can start reading from any frame

* Supports saving output images between frames

Tips:

- Click 'Select Video File' to select a video file

- Set relevant parameters

- Click 'Play'

- Press Q to exit

An actual example is shown below. [Video URL](https://www.bilibili.com/video/BV1cx411p7Lc?t=67)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200603163315833.gif#pic_center)

## Reference
[https://www.cnblogs.com/mengd/p/7287119.html](https://www.cnblogs.com/mengd/p/7287119.html)<br>
[Python Tkinter模块详解（后续持续补充）](https://blog.csdn.net/qq_42778168/article/details/97137618#Checkbutton%20%E5%A4%9A%E9%80%89%E6%A1%86%2FRadiobotton%20%E5%8D%95%E9%80%89%E6%A1%86)<br>
[【Python-opencv3.4】视频基本操作（帧率，总视频帧数、从第N帧开始播放、播放进度显示、按键控制视频）](https://blog.csdn.net/imwaters/article/details/90707336)
