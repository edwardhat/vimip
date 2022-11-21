import numpy as np 
import cv2 
import datetime

def getline(x0, y0, x1, y1):
    xys=[]
    if abs(x1-x0)>=abs(y1-y0):
        n = abs(x1-x0)
    else : 
        n = abs(y1-y0)

    dx = (x1-x0)/n
    dy = (y1-y0)/n
    x, y = x0, y0

    for k in range(n):
        xys.append( (int(x),int(y)) )
        x = x+dx
        y = y+dy
    return xys

def drawLine(canvas, x0, y0, x1, y1, color=(255, 255, 255)):
    xys = getline(x0, y0, x1, y1)
    for xy in xys:
        x, y = xy
        canvas[y, x, :] = color

def drawLinePQ(canvas, p, q, color):
    drawLine(canvas, p[0], p[1], q[0], q[1], color)
    return 

def drawPolygon(canvas, pts, color, isAxis=False, isStar=False):

    if isStar:
        for k in range(pts.shape[0]-2):
            drawLine(canvas, pts[k,0], pts[k,1], 
                            pts[k+2,0], pts[k+2,1], color)
        drawLinePQ(canvas, pts[-2], pts[0], color)
        drawLinePQ(canvas, pts[-1], pts[1], color)

    else:         
        for k in range(pts.shape[0]-1):
            drawLine(canvas, pts[k,0], pts[k,1], 
                            pts[k+1,0], pts[k+1,1], color)
        drawLinePQ(canvas, pts[-1], pts[0], color)

    if isAxis:
        center = np.array([0., 0])
        for p in pts:
            center += p 
        center = center / pts.shape[0]
        center = center.astype('int')
        drawLinePQ(canvas, center, pts[0], color)
    return 

def getRegularNGon(ngon):
    delta = 360. / ngon
    points = []
    for i in range(ngon):
        degree = i * delta 
        radian = deg2rad(degree)
        x = np.cos(radian)
        y = np.sin(radian)
        points.append( (x, y) )

    points = np.array(points)
    return points 

def deg2rad(deg):
    return (deg * np.pi / 180)

def Tmat(a,b):
    T = np.eye(3,3)
    T[0,2]=a
    T[1,2]=b
    return T

def Rmat(deg):
    rad = deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.eye(3,3)
    R[0,0] = c 
    R[0,1] = -s 
    R[1,0] = s 
    R[1,1] = c 
    return R

def H(pts):
    return np.vstack((pts, np.ones(pts.shape[1])))

def getRect(width,height):
    points=[]
    points.append( (-width/2, 0) )
    points.append( (width/2, 0) )
    points.append( (width/2, height) )
    points.append( (-(width/2), height) )

    points = np.array(points)
    return points

def main():
    width, height = 1400, 1000
    theta=0
    now = datetime.datetime.now()
    while True:
        canvas = np.zeros( (height, width, 3), dtype='uint8')
        points1 = (getRegularNGon(12)*300).T
        points2 = (getRect(20,270)).T
        points3 = (getRect(15,300)).T

        points1 = (Tmat(700,500) @ H(points1)).T[:,:2]
        points2 = (Tmat(700,500) @ Rmat(180+((now.hour%12)*30)+((now.minute)*0.5)) @ H(points2)).T[:,:2]
        points3 = (Tmat(700,500) @ Rmat(180+now.minute*6) @ H(points3)).T[:,:2]
        print(now.hour%12, now.minute)
    
        points1 = points1.astype('int')
        points2 = points2.astype('int')
        points3 = points3.astype('int')

        theta+=0.5
        cv2.circle(canvas, (700,500), 300, (255,255,255))
        drawPolygon(canvas, points2, (255,255,255))
        drawPolygon(canvas, points3, (255,255,255))
        drawPolygon(canvas, points1, (255,255,255))


        cv2.imshow("my window", canvas)
        if cv2.waitKey(20) == 27: break

if __name__ == "__main__":
    main()