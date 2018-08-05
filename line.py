import math

def is_in_range(x,y,line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    if x1 != x and x2 != x:
        if min(x1,x2,x) == x or max(x1,x2,x) == x:
            return False
    if y1 != y and y2 != y:
        if min(y1,y2,y) == y or max(y1,y2,y) == y:
            return False
    return True

def equation_of_line(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]

    infinite_slope = x1 == x2
    m = 0
    if not infinite_slope:
        m = (y2-y1)/(x2-x1)
        b = y1 - m*x1
        return (m,b)
    return (None,x1)

def is_in_range_vertical(y1,y2,y):
    return y>= min(y1,y2) and y<= max(y1,y2)

def line_intersection_same_slope(y1,y2,y3,y4):
    a1 = min(y1,y2)
    a2 = max(y1,y2)
    b1 = min(y2,y3)
    b2 = max(y2,y3)
    # line 1 is a1-a2 a2>=a1
    # line 2 is b1-b2 b2>=b1

    if a1 == b1 and a2 == b2: # both lines are same same l
        return a1,a2
    if is_in_range_vertical(a1,a2,b1):
       # b1 is point
        if is_in_range_vertical(a1,a2,b2):
            # b2 is also point
            return b1,b2
        else:
            return b1,a2
    elif is_in_range_vertical(a1,a2,b2):
        return a1,b2
    else:
        return None,None

def line_intersection(line1, line2):
    # find slope of fist line
    m1, b1 = equation_of_line(line1)
    m2, b2 = equation_of_line(line2)
    if m1 != None and m2 != None:
        # None of the lines are parallel to y-axis
        if m1 != m2:
            # sliopes are not equal
            x = (b2-b1)/(m1-m2)
            y = m1 * x + b1
        else:
            # slopes are equal and not parallel to y-axis
            # two case
            if b1 == b2:
                # y intercep are also  equal
                # two cases prallel to x axis
                x1, x2 = line_intersection_same_slope(line1[0][0], line1[1][0], line2[0][0], line2[1][0])
                x = x1
                y1, y2 = line_intersection_same_slope(line1[0][1], line1[1][1], line2[0][1], line2[1][1])
                y = y1
                # other wise
            else:
                # slopes are equal but differet y intercepts
                # so no intersection
                return None,None
    elif m1 == None and m2 == None:
        # Both lines are parallel to y axis
        x = line1[0][0]
        x1,x2 = line_intersection_same_slope(line1[0][0], line1[1][0], line2[0][0], line2[1][0])
        x = x1
        y1, y2 = line_intersection_same_slope(line1[0][1], line1[1][1], line2[0][1], line2[1][1])
        y = y1
    elif m1 == None:
        # line one is parallel to y -axis
        if b1 != None:
            x = b1
            y = m2 * x + b2
        else:
            return None,None
    else: # m2 == None:
        # line2 is parallel y-axis
        if b2 != None:
            x = b2
            y = m1 * x + b1
        else:
            return None,None

    if is_in_range(x, y,line1) and is_in_range(x, y,line2):
        return x, y
    else:
        return None, None

def main():
    line = [[98.04573113608151, 462.197068030155],[70.80499047146857, 433.13521234090973]]
    line2= [[80,450],[80,455]] # Parallel to y -axis but same x intercep
    line3= [[70,450],[70,455]] # Parallel to y -axis but same x intercep
    line4 = [[80,440],[100,440]] # same as s4
    line5 = [[85,440],[95,440]]
    line6 = [[5,5],[20,20]]

    s1 = [[80, 440], [80, 460]]
    s2 = [[80, 460], [100, 460]]
    s3 = [[100, 460], [100, 440]]
    s4 = [[100, 440], [80, 440]]
    diagonal = [[80, 460], [100, 440]]
    s5 = [[0,0],[50,50]]

    print(line_intersection(line6, s5))
    #print(line_intersection(line5,s1))
    #print(line_intersection(line5, s2))
    #print(line_intersection(line5, s3))
    #print(line_intersection(line5, s4))
    #print(line_intersection(line5, diagonal))



main()


