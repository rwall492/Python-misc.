import numpy as np

def read_data_trans(filename):
    f = np.genfromtxt(filename,delimiter=',',skip_header=1, dtype=None)

    trans = {}#dictionary with all info

    for x in f:
        key = x[0]
        trans.setdefault(key, [])
        trans[key].append((x[1],x[2]))

    return trans

def read_data_demo(filename,val):
    f = np.genfromtxt(filename,delimiter=',',skip_header=1, dtype=None)

    demo = {}#dictionary with one piece of demographic info 

    for x in f:
        key = x[0]
        demo.setdefault(key, [])
        demo[key].append(x[val])

    return demo
