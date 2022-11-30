import cv2
import os 
from pathlib import Path

cwd = os.path.dirname(__file__)
filename = Path(cwd) / 'chroma.mp4'
filename2 = Path(cwd) / 'raining.mp4'
vidcap1 = cv2.VideoCapture(str(filename)) 
vidcap2 = cv2.VideoCapture(str(filename2))
width = round(vidcap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = round(vidcap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_cnt1 = round(vidcap1.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(vidcap2.get(cv2.CAP_PROP_FRAME_COUNT))
fps = round(vidcap1.get(cv2.CAP_PROP_FPS))
recorder = cv2.VideoWriter("outputvid.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
delay = int(1000 / fps)

while vidcap1.isOpened():
    ret1, frame1 = vidcap1.read()
    ret2, frame2 = vidcap2.read() 
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (20, 150, 0), (70, 255, 255))
    cv2.copyTo(frame2, mask, frame1)
    cv2.imshow('frame', frame1)
    recorder.write(frame1)
    key = cv2.waitKey(delay)

recorder.release()