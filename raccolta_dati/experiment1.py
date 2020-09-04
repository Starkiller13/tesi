import numpy
import sys
from datetime import datetime
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import re
import math


if __name__ == "__main__":
    c = numpy.array([])
    d = numpy.array([])
    k = numpy.array([])
    tmp = numpy.array([])
    a = 0
    b = 0
    w = 0
    _rel = 0
    name = ''
    f = open(sys.argv[1], "r")
    for x in f:
        if 'MIP' in x:
            name = x.split()[1][0:-4]
        elif 'LP' in x:
            _rel = float(x.split()[3])
        elif x[0] == 'x':
            a = float(x.split()[1])
            b = float(x.split()[2])
            if a==-1 or b==-1:
                 c = numpy.append(c,float(1))
            else:
                if a-_rel!=0 :
                    a = a -_rel 
                else:
                    a = 0.01
                if b-_rel!=0 :
                    b = b -_rel 
                else:
                    b = 0.01
                c = numpy.append(c,math.pow(abs(a*b),float(1/2)))
    f.close()
    f = open(sys.argv[1], "r")
    for x in f:
            if 'clique constraint' in x :
                    w = 1
                    if len([value for value in tmp if value!=-1]) >0:
                        for y in tmp:
                            w = w*y
                        w = math.pow(abs(w),float(1/len(tmp)))
                        d = numpy.append(d,w)
                        k = numpy.append(k,numpy.max(tmp))
                        tmp = numpy.array([])
            elif x[0] == 'x' in x:
                b = float(x.split()[2])
                if b==-1:
                    tmp = numpy.append(tmp, float(1))
                else:
                    if b-_rel!=0 :
                        b = b -_rel 
                    else:
                        b = 0.01
                    tmp = numpy.append(tmp, b)
            elif 'All Zeroes' in x:
                b = float(x.split()[2])
                if b==-1:
                    tmp = numpy.append(tmp, 1)
                else:
                    if b-_rel!=0 :
                        b = b - _rel 
                    else:
                        b = 0.01
                    tmp = numpy.append(tmp, b)
                    
    w = 1
    if len([value for value in tmp if value!=-1]) >0:
        for y in tmp:
            w = w*y
        w = math.pow(abs(w),float(1/len(tmp)))
        d = numpy.append(d,w)
        k = numpy.append(k,numpy.max(tmp))
        tmp = numpy.array([])
    print(c)
    print(d)
    print(len(k))
    for x,y in enumerate(k):
        if y >= d[x-1]:
            plt.scatter(x,d[x], color='g')
        else:
            plt.scatter(x,d[x], color='r')
    plt.title(name) 
    red_patch = mpatches.Patch(color='red', label='Index worst than\ns.v. separation')
    green_patch = mpatches.Patch(color='green', label='Index better than\ns.v. separation')
    plt.legend(handles=[red_patch,green_patch])
    plt.xticks(ticks = range(len(d)))
    plt.xlabel('clique') 
    plt.ylabel("index value") 
    plt.savefig("chart_exp1_"+name+".jpg")
    f.close()