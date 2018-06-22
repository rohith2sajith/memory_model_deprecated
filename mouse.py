import numpy as np
import math
class Mouse(object):
    ALPHA = 0.875
    SIGMA = 0.707
    MEAN = 0
    MIN = 0.5

    def __init__(self,x,y,v,a,t):
        self.x=x
        self.y=y
        self.v=v
        self.a=a
        self.t=t

    def get_next_acceleration(self):
        a =  np.random.normal(self.MEAN,self.SIGMA)
        return a

    def get_next_velocity(self, v,a,t):
        if t == 0:
            return self.ALPHA+1
        arr = [math.pow(a,t)]
        for num in range(t-1):
            arr.append(0)
        arr.append(self.ALPHA)
        arr.append(-1)
        y = np.polynomial.polynomial.polyroots(arr)
        for i in y:
            print(i.real, i.imag)
        return np.polynomial.polynomial.polyroots(arr)



    def get_next_coordinate(self, x, y, v, t):
        theta = np.random.random() * 180
        v_x = v * np.cos(theta)
        v_y = v * np.sin(theta)
        if t==0:
            return [1+v_x,1+v_y]
        valsx = [math.pow(v_x,t + 1)]
        valsy = [math.pow(v_y,t + 1)]
        for num in range(t - 1):
            valsx.append(0)
            valsy.append(0)
        valsx.append(1)
        valsx.append(-1)
        valsy.append(1)
        valsy.append(-1)
        return [np.polynomial.polynomial.polyroots(valsx),
                np.polynomial.polynomial.polyroots(valsy)]

    def get_x (self):
        return self.x


    def get_y(self):
        return self.y


    def get_v(self):
        return self.v

    def get_a(self):
        return self.a

    def get_t(self):
        return self.t

    def set_x(self, x):
        self.x = x


    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_v(self, v):
        self.v = v

    def set_a(self, a):
        self.a = a


    def set_t(self, t):
        self.t = t

    def __str__(self):
        return f"x={self.x},y={self.y}"


