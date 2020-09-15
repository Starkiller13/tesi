from os import listdir
import numpy
import math
from matplotlib import pyplot as plt 
from os.path import isfile, join
onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
num = numpy.array([],dtype="i")
den = numpy.array([],dtype="i")
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
                    if a-_rel!=0:
                        a = a -_rel 
                    else:
                        a = 0.01
                    if b-_rel!=0:
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
                        if b-_rel!=0:
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
        tmp = [value for value in d if value > numpy.max(c) ]
        num = numpy.append(num,int(len(tmp)))
        den = numpy.append(den,int(len(d)))
print(num)
print(den)
plt.figure(figsize =(8,6))
rects1 = plt.bar(files,num,width=.4, label="# of good cliques")
rects2 = plt.bar([0.4+ value for value, c in enumerate(den)],den,width=.4, label = "# of cliques" )
plt.bar([0.8 + value for value, c in enumerate(files)],numpy.zeros(len(files)),width=.2)
plt.xticks(files,rotation=45)
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',rotation=90)
autolabel(rects1)
autolabel(rects2)
plt.legend()
plt.savefig("chart_agg2.jpg")