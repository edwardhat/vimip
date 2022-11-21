import numpy as np 
import cv2
def main():
    width, height = 1400, 1000
    stars = []
    while True:
        canvas = np.zeros( (height, width, 3), dtype='uint8')
        a=np.random.randint(0,1399)
        b=np.random.randint(0,999)
        stars.append((b,a))
        for x in stars:
            canvas[x[0],x[1]]=np.random.randint(0,255,3)
        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27: break

if __name__ == "__main__":
    main() 