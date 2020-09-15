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
    u = numpy.array([])
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
                pass
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
                    if len(tmp) >0:
                        for y in tmp:
                            w = w*math.pow(abs(y),float(1/len(tmp)))
                        d = numpy.append(d,w)
                        k = numpy.append(k,math.pow(numpy.max(u),1/2))
                        tmp = numpy.array([])
                        u = numpy.array([])
            elif x[0] == 'x' in x:
                b = float(x.split()[2])
                if b==-1:
                    pass
                else:
                    if b-_rel!=0 :
                        b = b -_rel 
                    else:
                        b = 0.01
                    tmp = numpy.append(tmp, b) 
                a = float(x.split()[1])
                b = float(x.split()[2])
                if a-_rel!=0 :
                    a = a -_rel 
                else:
                    a = 0.01
                if b-_rel!=0 :
                    b = b -_rel 
                else:
                    b = 0.01
                u = numpy.append(u, abs(b*a))
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
    if len(tmp) >0:
        for y in tmp:
            w = w*math.pow(abs(y),float(1/len(tmp)))
        d = numpy.append(d,w)
        k = numpy.append(k,math.pow(numpy.max(u),1/2))
        tmp = numpy.array([])
        u = numpy.array([])
    print(c)
    print(d)
    print(k)
    print(len(k))
    j=0
    plt.figure(figsize =(8,7))
    for y in k:
        if d[j]<numpy.max(k):
            plt.scatter(j+1,d[j], color='r')
        else:
            plt.scatter(j+1,d[j], color='g')
        j = j+1
    plt.title(name) 

    plt.plot([1, len(d)],[numpy.max(k),numpy.max(k)])
    blue_patch = mpatches.Patch(color='blue', label = "Best Strong Branching Index ")
    red_patch = mpatches.Patch(color='red', label='Index worst than\nBest SB')
    green_patch = mpatches.Patch(color='green', label='Index better than\nBest SB')
    plt.legend(handles=[green_patch, red_patch, blue_patch])
    
    plt.xticks(ticks = range(len(d))+numpy.ones(len(d)), rotation = 75)
    plt.xlabel('clique') 
    plt.ylabel("separation index value") 
    plt.savefig("chart_exp1_"+name+".jpg")
    f.close()