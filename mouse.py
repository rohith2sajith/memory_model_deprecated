import numpy as np
import math
import maze
from sympy import *
from sympy.geometry import *
import config as config
from datetime import datetime

class Mouse(object):

    def __init__(self,x,y,v_x,v_y,t,memorymodel):
        self.x=x
        self.y=y
        self.v_x=v_x
        self.v_y=v_y
        self.t=t
        self.memorymodel = memorymodel
        self.mouse_shape = None
        self.distance = 0

    def get_next_acceleration_x(self):
        a_x = np.random.normal(config.MEAN,config.SIGMA1/(math.pow(2,1/2)))
        return a_x

    def get_next_acceleration_y(self):
        a_y = np.random.normal(config.MEAN,config.SIGMA1/(math.pow(2,1/2)))
        return a_y

    def get_next_acceleration2_x(self):
        a_x = np.random.normal(config.MEAN,config.SIGMA2/(math.pow(2,1/2)))
        return a_x

    def get_next_acceleration2_y(self):
        a_y = np.random.normal(config.MEAN,config.SIGMA2/(math.pow(2,1/2)))
        return a_y

    def get_next_velocity_x(self):
        new_v_x = config.ALPHA*self.get_v_x()+self.get_next_acceleration_x()
        self.set_v_x(new_v_x)
        return new_v_x

    def get_next_velocity_y(self):
        new_v_y = config.ALPHA*self.get_v_y() + self.get_next_acceleration_y()
        self.set_v_y(new_v_y)
        return new_v_y

    def get_next_velocity2_y(self):
        new_v_y = config.ALPHA*self.get_v_y() + self.get_next_acceleration2_y()
        self.set_v_y(new_v_y)
        return new_v_y

    def get_next_velocity2_x(self):
        new_v_x = config.ALPHA*self.get_v_x()+self.get_next_acceleration2_x()
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
        if abs(y_f-y) > config.MAX_Y:
            if y > y_f:
                y_f = y - config.MAX_Y
            else:
                y_f = y + config.MAX_Y
        return [x_f,y_f]

    def get_row(self):
        return self.get_y()//config.CELL_WIDTH

    def get_col(self):
        return self.get_x()//config.CELL_WIDTH


    def off_grid(self,x_f,y_f):
        if x_f < 0:
            return [True,0]
        elif x_f > config.BOARD_MAX:
            return [True,1]
        elif y_f < 0:
            return [True,2]
        elif y_f > config.BOARD_MAX:
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
        if x + d_x > config.BOARD_MAX:
            x_f = x - d_x
        if y + d_y > config.BOARD_MAX:
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
    @staticmethod
    def intersect2( a, b, c, d, lower_x, lower_y):

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
        #p1 = Point2D(a, b)
        #p2 = Point2D(c, d)
        if a == c and b == d:
            return [False, 0,0]

        given_segment = [[a,b],[c,d]]#Segment2D(p1, p2) # given segment
        # create segments for each of the four edges
        s1 = [[lower_x, lower_y],[lower_x, lower_y+config.CELL_WIDTH]]#Segment2D((lower_x, 0), (lower_x, 2))
        s2 = [[lower_x, lower_y+config.CELL_WIDTH],[lower_x + config.CELL_WIDTH, lower_y+config.CELL_WIDTH]] #Segment2D((lower_x + 20, 0), (lower_x + 20, 2))
        s3 = [[lower_x + config.CELL_WIDTH, lower_y+config.CELL_WIDTH],[lower_x + config.CELL_WIDTH, lower_y]] #Segment2D((0, lower_y), (2, lower_y))
        s4 = [[lower_x + config.CELL_WIDTH, lower_y],[lower_x, lower_y]]#Segment2D((0, lower_y + 20), (2, lower_y + 20))

        int_point_list=[]
        # check each segment intersection with given segment
        # if intersect return True and x and y cordinated
        x,y = config.line_intersection(given_segment,s1)

        if x != None:
            int_point_list.append([x,y])

        x,y = config.line_intersection(given_segment, s2)
        if x != None:
            int_point_list.append([x,y])

        x,y = config.line_intersection(given_segment, s3)
        if x != None:
            int_point_list.append([x,y])

        x,y = config.line_intersection(given_segment, s4)
        if x != None:
            int_point_list.append([x,y])
        if len(int_point_list):
            ret_list = [True]
            ret_list.append(int_point_list)
            return ret_list
        return [False]


    def move(self,x,y):
        current_x = self.x  # store old x and y
        current_y = self.y
        # draw line
        distance = math.sqrt(math.pow(x-current_x,2)+math.pow(y-current_y,2))
        self.distance += distance
        #config.pl(f"drawing line ({current_x},{current_y}) - ({x},{y}) - {distance}")
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

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance



    def set_t(self, t):
        self.t = t

    def __str__(self):
        return f"x={self.x},y={self.y}"


