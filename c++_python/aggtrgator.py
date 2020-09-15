from os import listdir
import numpy
from scipy.stats import gmean
import math
from matplotlib import pyplot as plt 
from os.path import isfile, join
onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
num = numpy.array([])
den = numpy.array([])
files = numpy.array([])
for fil in onlyfiles:
    if ".mps" in fil:
        c = numpy.array([])
        d = numpy.array([])
        tmp = numpy.array([])
        a = 0
        b = 0
        w = 0
        _rel = 0
        name = ''
        f = open(fil,"r")
        for x in f:
            if 'MIP' in x:
                name = x.split()[1][0:-4]
                files = numpy.append(files, name)
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
        f = open(fil, "r")
        for x in f:
                if 'clique constraint' in x :
                        w = 1
                        if len(tmp) >0:
                            for y in tmp:
                                w = w*math.pow(abs(y),float(1/len(tmp)))
                            d = numpy.append(d,w)
                            tmp = numpy.array([])
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
                elif 'All Zeroes' in x:
                    b = float(x.split()[2])
                    if b==-1:
                        pass
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
            tmp = numpy.array([])
        f.close()
        num = numpy.append(num, numpy.max(d))
        den = numpy.append(den, numpy.max(c))
print(num)
print(den)
r = num / den
print (r)
print(gmean(r))
plt.figure(figsize =(8,6))
plt.plot(files,numpy.ones(len(files)), color = 'r', label = "treshold value")
plt.plot(files,gmean(r)*numpy.ones(len(files)),color = 'g', label = "geometric mean: "+ str(gmean(r))[:5])
plt.scatter(files,r, label = "problem ratio")
plt.legend()
plt.yscale('symlog')
plt.xticks(files,rotation=45)
plt.ylabel("separation index ratio") 
plt.savefig("chart_agg.jpg")