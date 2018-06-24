import numpy as np
import math
import maze
class Mouse(object):
    ALPHA = 10
    SIGMA = 1.5
    MEAN = 0
    MIN = 0.5

    def __init__(self,x,y,v,a,t,memorymodel):
        self.x=x
        self.y=y
        self.v=v
        self.a=a
        self.t=t
        self.memorymodel = memorymodel
        self.mouse_shape = None

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

        z = np.polynomial.polynomial.polyroots(arr)
        k = z.imag
        for i in range(t+1):
            if k[i] == 0:
                return z[i].real

        return 2


        #return np.polynomial.polynomial.polyroots(arr)

    #def get_next_coordinate(self, x, y, v, t):
     #   theta = np.random.random() * 180
      #  v_x = v * np.cos(theta)
       # v_y = v * np.sin(theta)
        #if t==0:
         #   return [1+v_x,1+v_y]
       # valsx = [math.pow(v_x,t + 1)]
#        valsy = [math.pow(v_y,t + 1)]
 #       for num in range(t - 1):
  #          valsx.append(0)
   #         valsy.append(0)
    #    valsx.append(1)
     #   valsx.append(-1)
      #  valsy.append(1)
       # valsy.append(-1)
#        X = np.polynomial.polynomial.polyroots(valsx)
 #       Y = np.polynomial.polynomial.polyroots(valsy)
  #      X_i = X.imag
   #     Y_i = Y.imag
    #    XX = 2
     #   YY = 2
      #  for i in range(t+1):
       #     if X_i[i] == 0:
        #        XX = X[i].real
#
 #       for j in range(t+1):
  #          if Y_i[j] == 0:
   #             YY = Y[i].real
#
 #       return [XX, YY]

    def get_next_coordinate(self, x, y, t):
        theta = np.random.random() * 180
        d = np.random.random() * 10
        d_x = d * np.cos(theta)
        d_y = d * np.sin(theta)
        x_f = x+ d_x
        y_f = y + d_y
        if x+d_x < 0:
            x_f = x - d_x
        if y+d_y < 0:
            y_f = y - d_y
        if x + d_x > 600:
            x_f = x - d_x
        if y + d_y > 600:
            y_f = y - d_y


        return [x_f,y_f]

    def intersect(self,a,b,c,d,lower_x,lower_y):
        slope = (d-b)/(c-a)
        rslope = (c-a)/(d-b)
        nslope= (b-d)/(c-a)
        nrslope= (a-c)/(d-b)
        if (nslope*(lower_x)-c*nslope+d) < lower_y + 20 and (nslope*(lower_x)-c*nslope+d) > lower_y and int(lower_x) in range(int(min(a,c)),int(max(a,c)+1)):
            return True
        elif (nslope*(lower_x+20)-c*nslope+d) < lower_y + 20 and (nslope*(lower_x+20)-c*nslope+d) > lower_y and int(lower_x)+20 in range(int(min(a,c)),int(max(a,c)+1)):
            return True
        elif ((lower_y-d)*nrslope+c) < lower_x+20 and ((lower_y-d)*nrslope+c) > lower_x and int(lower_y) in range(int(min(b,d)),int(max(b,d)+1)):
            return True
        elif ((lower_y+20-d)*nrslope+c) < lower_x+20 and ((lower_y+20-d)*nrslope+c) > lower_x and int(lower_y)+20 in range(int(min(b,d)),int(max(b,d)+1)):
            return True
        else:
            return False







    def move(self,x,y):
        current_x = self.x  # store old x and y
        current_y = self.y
        # draw line
        self.memorymodel.draw_line(current_x,current_y,x,y)
        #print(f"drawing line ({current_x},{current_y}) - ({x},{y})")
        self.mouse_shape = self.memorymodel.update_circle(self.mouse_shape,x,y)
        self.set_x(x) # save x an y
        self.set_y(y)

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


