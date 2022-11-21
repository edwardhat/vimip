import numpy as np 
import cv2 

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

def RectJoint(pts):
    return np.array( ((pts[2][0]+pts[3][0])/2 ,  (pts[2][1]+pts[3][1])/2) )

def angleBetweenVector(v1, v2):
    uvec1 = v1 / np.linalg.norm(v1)
    uvec2 = v2 / np.linalg.norm(v2)
    return np.arctan2(np.cross(uvec1, uvec2), np.dot(uvec1, uvec2))

def invKinematics(current,tip,goal,angle):
    angle += angleBetweenVector(tip-current,goal-current)
    return angle

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

def getRect(width,height):
    points=[]
    points.append( (-width/2, 0) )
    points.append( (width/2, 0) )
    points.append( (width/2, height) )
    points.append( (-(width/2), height) )

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

def main():

    width, height = 1400, 1000
    alpha=0
    beta=0
    gamma=0
    theta=0
    eps = 0
    color = (255,255,255)
    goal = np.array((430,490))
    while True:
        canvas = np.zeros( (height, width, 3), dtype='uint8')

        sarm1 = getRect(30,130).T
        sarm2 = getRect(20,100).T
        sarm3 = getRect(16,80).T
        sarm4 = getRect(14,60).T
        sarm5 = getRect(10,40).T
        
        arm1 = (Tmat(700,500) @ Rmat(alpha) @ H(sarm1)).T[:,:2]
        arm2 = (Tmat(RectJoint(arm1)[0], RectJoint(arm1)[1]) @ Rmat(beta) @ H(sarm2)).T[:,:2]
        arm3 = (Tmat(RectJoint(arm2)[0], RectJoint(arm2)[1]) @ Rmat(gamma) @ H(sarm3)).T[:,:2]
        arm4 = (Tmat(RectJoint(arm3)[0], RectJoint(arm3)[1]) @ Rmat(theta) @ H(sarm4)).T[:,:2]
        arm5 = (Tmat(RectJoint(arm4)[0], RectJoint(arm4)[1]) @ Rmat(eps) @ H(sarm5)).T[:,:2]

        eps = invKinematics(RectJoint(arm4),RectJoint(arm5),goal,eps)
        arm5 = (Tmat(RectJoint(arm4)[0], RectJoint(arm4)[1]) @ Rmat(eps) @ H(sarm5)).T[:,:2]

        theta = invKinematics(RectJoint(arm3),RectJoint(arm5),goal,theta)
        arm4 = (Tmat(RectJoint(arm3)[0], RectJoint(arm3)[1]) @ Rmat(theta) @ H(sarm4)).T[:,:2]
        arm5 = (Tmat(RectJoint(arm4)[0], RectJoint(arm4)[1]) @ Rmat(eps) @ H(sarm5)).T[:,:2]

        gamma = invKinematics(RectJoint(arm2),RectJoint(arm5),goal,gamma)
        arm3 = (Tmat(RectJoint(arm2)[0], RectJoint(arm2)[1]) @ Rmat(gamma) @ H(sarm3)).T[:,:2]
        arm4 = (Tmat(RectJoint(arm3)[0], RectJoint(arm3)[1]) @ Rmat(theta) @ H(sarm4)).T[:,:2]
        arm5 = (Tmat(RectJoint(arm4)[0], RectJoint(arm4)[1]) @ Rmat(eps) @ H(sarm5)).T[:,:2]

        beta = invKinematics(RectJoint(arm1),RectJoint(arm5),goal,beta)
        arm2 = (Tmat(RectJoint(arm1)[0], RectJoint(arm1)[1]) @ Rmat(beta) @ H(sarm2)).T[:,:2]
        arm3 = (Tmat(RectJoint(arm2)[0], RectJoint(arm2)[1]) @ Rmat(gamma) @ H(sarm3)).T[:,:2]
        arm4 = (Tmat(RectJoint(arm3)[0], RectJoint(arm3)[1]) @ Rmat(theta) @ H(sarm4)).T[:,:2]
        arm5 = (Tmat(RectJoint(arm4)[0], RectJoint(arm4)[1]) @ Rmat(eps) @ H(sarm5)).T[:,:2]
        
        alpha = invKinematics((700,500),RectJoint(arm5),goal,alpha)
        arm1 = (Tmat(700,500) @ Rmat(alpha) @ H(sarm1)).T[:,:2]
        arm2 = (Tmat(RectJoint(arm1)[0], RectJoint(arm1)[1]) @ Rmat(beta) @ H(sarm2)).T[:,:2]
        arm3 = (Tmat(RectJoint(arm2)[0], RectJoint(arm2)[1]) @ Rmat(gamma) @ H(sarm3)).T[:,:2]
        arm4 = (Tmat(RectJoint(arm3)[0], RectJoint(arm3)[1]) @ Rmat(theta) @ H(sarm4)).T[:,:2]
        arm5 = (Tmat(RectJoint(arm4)[0], RectJoint(arm4)[1]) @ Rmat(eps) @ H(sarm5)).T[:,:2]



        arm1 = arm1.astype('int')
        arm2 = arm2.astype('int')
        arm3 = arm3.astype('int')
        arm4 = arm4.astype('int')
        arm5 = arm5.astype('int')


        drawPolygon(canvas, arm1, color)
        drawPolygon(canvas, arm2, color)
        drawPolygon(canvas, arm3, color)
        drawPolygon(canvas, arm4, color)
        drawPolygon(canvas, arm5, color)
        cv2.circle(canvas, goal, 5, (0,0,255))
        cv2.imshow("my window", canvas)

        # change the goal position on different inputs
        t = cv2.waitKey(20)
        if t == 27: break
        if t == ord('a'):
            print("pressed a")
            goal += (-10,0)
        elif t == ord('w'):
            print("pressed w")
            goal += (0,-10)
        elif t == ord('s'):
            print("pressed s")
            goal += (0,10)
        elif t == ord('d'):
            print("pressed d")
            goal += (10,0)

if __name__ == "__main__":
    main()