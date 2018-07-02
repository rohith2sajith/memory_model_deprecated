import numpy as np
import math
import maze
from sympy import *
from sympy.geometry import *
import config as config

class Mouse(object):
    ALPHA = 0.875
    SIGMA1 = 5.6
    SIGMA2 = 5.6
    MEAN = 0
    MIN = 0.5

    def __init__(self,x,y,v_x,v_y,t,memorymodel):
        self.x=x
        self.y=y
        self.v_x=v_x
        self.v_y=v_y
        self.t=t
        self.memorymodel = memorymodel
        self.mouse_shape = None

    def get_next_acceleration_x(self):
        a_x = np.random.normal(self.MEAN,self.SIGMA1/(math.pow(2,1/2)))
        return a_x

    def get_next_acceleration_y(self):
        a_y = np.random.normal(self.MEAN,self.SIGMA1/(math.pow(2,1/2)))
        return a_y

    def get_next_acceleration2_x(self):
        a_x = np.random.normal(self.MEAN,self.SIGMA2/(math.pow(2,1/2)))
        return a_x

    def get_next_acceleration2_y(self):
        a_y = np.random.normal(self.MEAN,self.SIGMA2/(math.pow(2,1/2)))
        return a_y

    def get_next_velocity_x(self):
        new_v_x = self.ALPHA*self.get_v_x()+self.get_next_acceleration_x()
        self.set_v_x(new_v_x)
        return new_v_x

    def get_next_velocity_y(self):
        new_v_y = self.ALPHA*self.get_v_y() + self.get_next_acceleration_y()
        self.set_v_y(new_v_y)
        return new_v_y

    def get_next_velocity2_y(self):
        new_v_y = self.ALPHA*self.get_v_y() + self.get_next_acceleration2_y()
        self.set_v_y(new_v_y)
        return new_v_y

    def get_next_velocity2_x(self):
        new_v_x = self.ALPHA*self.get_v_x()+self.get_next_acceleration2_x()
        self.set_v_x(new_v_x)
        return new_v_x

    def get_next_coor(self,x,y):
        x_f = x+self.get_next_velocity_x()
        y_f = y+self.get_next_velocity_y()
        return [x_f, y_f]

    def get_next_coor2(self,x,y):
        x_f = x+self.get_next_velocity2_x()
        y_f = y+self.get_next_velocity2_y()
        return [x_f, y_f]

    def get_next_coor_directed(self,x,y,theta):
        x_f = self.get_next_coor2(x,y)[0]
        y_f = y + self.get_v_x()* np.tan(theta)
        if abs(y_f-y) > 30:
            if y > y_f:
                y_f = y - 30
            else:
                y_f = y + 30
        return [x_f,y_f]


    def off_grid(self,x_f,y_f):
        if x_f < 0:
            return [True,0]
        elif x_f > 600:
            return [True,1]
        elif y_f < 0:
            return [True,2]
        elif y_f > 600:
            return [True,3]
        else:
            return [False,0]


    def get_next_coordinate(self, x, y, t):
        theta = (np.random.random() * 90)+270
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
        p1 = Point2D(a,b)
        p2 = Point2D(c,d)
        if a == c and b == d:
            return [False,0]
        line = Line2D(p1,p2)
        if int(intersection(line,Line2D((lower_x,0),(lower_x,2)))[0].y) in range (int(lower_y),int(lower_y)+20+1) and int(lower_x) in range(int(min(a,c)),int(max(a,c)+1)):
            return [True,0]
        elif int(intersection(line,Line2D((lower_x+20,0),(lower_x+20,2)))[0].y) in range (int(lower_y),int(lower_y)+20+1) and int(lower_x)+20 in range(int(min(a,c)),int(max(a,c)+1)):
            return [True,1]
        elif int(intersection(line,Line2D((0,lower_y),(2,lower_y)))[0].x) in range (int(lower_x),int(lower_x)+20+1) and int(lower_y) in range(int(min(b,d)),int(max(b,d)+1)):
            return [True,2]
        elif int(intersection(line,Line2D((0,lower_y+20),(2,lower_y+20)))[0].x) in range (int(lower_x),int(lower_x)+20+1) and int(lower_y)+20 in range(int(min(b,d)),int(max(b,d)+1)):
            return [True,3]
        else:
            return [False,0]

    def intersect2(self, a, b, c, d, lower_x, lower_y):

        # if not interseaction it will return [False]
        # if there is one interection it will return [True, [ [x1,y1] ] ]
        # if there is two intersection points it will return [True, [ [x1,y1], [x2,y2] ]
        # like that
        #  Calling intersect2
        #  int_result = intersect2(......)
        #  if int_result[0]: # meaning you have one or more inter
        #  for coord_point in   int_result[1]:
        #     x = coord_point[0]
        #     y = coord_point[1]

        p1 = Point2D(a, b)
        p2 = Point2D(c, d)
        if a == c and b == d:
            return [False, 0,0]

        given_segment = Segment2D(p1, p2) # given segment
        # create segments for each of the four edges
        s1 = Segment2D((lower_x, 0), (lower_x, 2))
        s2 = Segment2D((lower_x + 20, 0), (lower_x + 20, 2))
        s3 = Segment2D((0, lower_y), (2, lower_y))
        s4 = Segment2D((0, lower_y + 20), (2, lower_y + 20))

        int_point_list=[]
        # check each segment intersection with given segment
        # if intersect return True and x and y cordinated
        int_points = intersection(given_segment,s1)
        if int_points and len(int_points):
            int_point_list.append([float(int_points[0].x),float(int_points[0].y)])

        int_points = intersection(given_segment, s2)
        if int_points and len(int_points):
            int_point_list.append([float(int_points[0].x), float(int_points[0].y)])

        int_points = intersection(given_segment, s3)
        if int_points and len(int_points):
            int_point_list.append([float(int_points[0].x), float(int_points[0].y)])

        int_points = intersection(given_segment, s4)
        if int_points and len(int_points):
            int_point_list.append([float(int_points[0].x),float(int_points[0].y)])
        if len(int_point_list):
            return [True].append(int_point_list)
        return [False]



    def move(self,x,y):
        current_x = self.x  # store old x and y
        current_y = self.y
        # draw line
        distance = math.sqrt(math.pow(x-current_x,2)+math.pow(y-current_y,2))
        config.pl(f"drawing line ({current_x},{current_y}) - ({x},{y}) - {distance}")
        self.memorymodel.draw_line(current_x,current_y,x,y)
        self.mouse_shape = self.memorymodel.update_circle(self.mouse_shape,x,y)
        self.set_x(x) # save x an y
        self.set_y(y)

    def get_x (self):
        return self.x


    def get_y(self):
        return self.y


    def get_v_x(self):
        return self.v_x

    def get_v_y(self):
        return self.v_y


    def get_t(self):
        return self.t

    def set_x(self, x):
        self.x = x


    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_v_x(self, v_x):
        self.v_x = v_x

    def set_v_y(self, v_y):
        self.v_y = v_y



    def set_t(self, t):
        self.t = t

    def __str__(self):
        return f"x={self.x},y={self.y}"


