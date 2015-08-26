fp_path = 'func_call_graph.viki'

fp = open(fp_path, 'r')
count = 0
nodes = []
#DEBUG = True
DEBUG = False
while True:
    line = fp.readline()
    if not line:
        print ("EOF")
        break
    elif line.startswith('node'):
        title = line.split(' ')[3][1:-1]
        label = line.split(' ')[5][1:-1]
        tmp = {"title":title, "label":label}
        nodes.append(tmp)
        if DEBUG:
            print("title: {0}".format(title))
            print("label: {0}".format(label))
            count += 1
            if count == 100:
                print ("counting down")
                break
    else:
        continue
fp.close()

dimension = len(nodes)
print "dimension: {0}".format(dimension)
import numpy as np
M = np.zeros((dimension, dimension))
#print M
fp = open(fp_path, 'r')
count = 0
while True:
    line = fp.readline()
    if not line:
        break
    elif line.startswith('edge'):
        row = line.split(' ')[3][1:-1]
        colum = line.split(' ')[5][1:-1]
        M[int(row)][int(colum)] = 1
        if DEBUG:
            print("row: {0}".format(row))
            print("colum: {0}".format(colum))
            count += 1
            if count == 100:
                break
    else:
        continue

#print M
"""
import pylab
pylab.plot(M)
pylab.show()
"""

import matplotlib.pyplot as pt
print M[0:100, 0:100]
pt.plot(M[0:100, 0:100])
pt.show()
