import csv
import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

def run():
    f = np.genfromtxt('astudentData.csv',delimiter=',',skip_header=1,dtype=(float,float,float))#long term, change this to variable input
    
    stuff = []
    num = []
    frac = []

    sum_correct = 0
    sum_response = 0
    counter = 0

    q_id = 0
    u_id = 0
    ans = 0
    q_last = 0

    entries = 0

    for x in f:
        question_id, user_id, correct = x

        q_id = x[0]
        u_id = x[1]
        ans = x[2]

        if entries == 0:
            q_last = q_id
        if q_id == q_last:
        #still filling from current question
            sum_correct += ans
            sum_response += 1
        else:
        #have moved on to a new question so store info an move on
            f = sum_correct / sum_response
            s = np.sqrt(f * (1.0 - f) / sum_response)
            stuff.append([q_id, f, s, sum_response])
            sum_correct = ans
            sum_response = 1
            counter += 1#unique, incremental identifier of question ID
        q_last = q_id #increment last question ID number
        entries += 1 #probably a better way to do this ....

    #first, we code the SVM method
    num_frac = [[i[3],i[1]] for i in stuff]#create the data set for SVC

    t_svm = svm.SVC(random_state=0,kernel='linear')#fix random number generator seed for reproducable results

    target = []
    t_data = []

    random.seed(1)#fix random number generator seed for reproducable results

    density = 0.125 * (525.0 / 200.0) #a choice, but ensures equal density of training points for each category

    #populate training data .. done by hand, but could be better to scale up
    x1 = (2500, 3500)
    y1 = (0.55,0.65)

    tx1 = []
    ty1 = []
    
    r1 = int(density * (x1[1] - x1[0]) * (y1[1] - y1[0]))
    for x in range(r1):
        target.append(0)
        t_data.append([random.uniform(x1[0],x1[1]),random.uniform(y1[0],y1[1])])
        tx1.append(random.uniform(x1[0],x1[1]))
        ty1.append(random.uniform(y1[0],y1[1]))

    x2 = (0, 2500)
    y2 = (0.35,0.85)

    tx2 = []
    ty2 = []

    r2 = int(density * (x2[1] - x2[0]) * (y2[1] - y2[0]))
    for x in range(r2):
        target.append(1)
        t_data.append([random.uniform(x2[0],x2[1]),random.uniform(y2[0],y2[1])])
        tx2.append(random.uniform(x2[0],x2[1]))
        ty2.append(random.uniform(y2[0],y2[1]))

    x3 = (0, 3500)
    y3 = (0.0,0.35)

    tx3 = []
    ty3 = []

    r3 = int(density * (x3[1] - x3[0]) * (y3[1] - y3[0]))
    for x in range(r3):
        target.append(2)
        t_data.append([random.uniform(x3[0],x3[1]),random.uniform(y3[0],y3[1])])
        tx3.append(random.uniform(x3[0],x3[1]))
        ty3.append(random.uniform(y3[0],y3[1]))

    x4 = (0, 3500)
    y4 = (0.85,1.0)

    tx4 = []
    ty4 = []

    r4 = int(density * (x4[1] - x4[0]) * (y4[1] - y4[0]))
    for x in range(r4):
        target.append(3)
        t_data.append([random.uniform(x4[0],x4[1]),random.uniform(y4[0],y4[1])])
        tx4.append(random.uniform(x4[0],x4[1]))
        ty4.append(random.uniform(y4[0],y4[1]))

    x5 = (2500, 3500)
    y5 = (0.65,0.85)

    tx5 = []
    ty5 = []

    r5 = int(density * (x5[1] - x5[0]) * (y5[1] - y5[0]))
    for x in range(r5):
        target.append(4)
        t_data.append([random.uniform(x5[0],x5[1]),random.uniform(y5[0],y5[1])])
        tx5.append(random.uniform(x5[0],x5[1]))
        ty5.append(random.uniform(y5[0],y5[1]))

    x6 = (2500, 3500)
    y6 = (0.35,0.55)

    tx6 = []
    ty6 = []

    r6 = int(density * (x6[1] - x6[0]) * (y6[1] - y6[0]))
    for x in range(r6):
        target.append(5)
        t_data.append([random.uniform(x6[0],x6[1]),random.uniform(y6[0],y6[1])])
        tx6.append(random.uniform(x6[0],x6[1]))
        ty6.append(random.uniform(y6[0],y6[1]))

    plt.figure()
    plt.xlabel('Questions asked []')
    plt.ylabel('Fraction of correct responses')
    plt.plot(tx1,ty1,'go',tx2,ty2,'go',tx3,ty3,'ro',tx4,ty4,'ro',tx5,ty5,'ro',tx6,ty6,'ro')
    plt.savefig('plots/test_data.eps')
    #sanity check plot 1

    t_svm.fit(t_data,target)

    res = t_svm.predict(num_frac)

    num_pass = []
    frac_pass = []

    num_fail = []
    frac_fail = []

    pass_svm = []

    print 'Good questions:'
    for x in range (len(res)):
        if res[x] == 0 or res[x] == 1:
            num_pass.append(num_frac[x][0])
            frac_pass.append(num_frac[x][1])
            pass_svm.append(stuff[x][0])
            print stuff[x][0]
        else:
            num_fail.append(num_frac[x][0])
            frac_fail.append(num_frac[x][1])

    print ' '
    print 'Num good, num bad: ', len(num_pass), len(num_fail)
    print ' '
    print '***********************************************'

    plt.figure()
    plt.xlabel('Questions asked []')
    plt.ylabel('Fraction of correct responses')
    plt.plot(num_fail,frac_fail,'ro',num_pass,frac_pass,'go')
    plt.savefig('plots/frac_vs_num_scatter.eps')
    #results of SVM

    #now write code for the weight method
    means = [i[1] for i in stuff]
    mu = np.sum(means) / len(means)

    print 'Weights for each question: '

    weights = []
    for x in range (len(stuff)):
        if stuff[x][2] > 0:
            w = np.exp(-1.0 * abs(stuff[x][1] - mu) / stuff[x][2])
        else:
            w = 0
        weights.append(w)
        print stuff[x][0], w

    dummy = [float(1)] * len(pass_svm)
    s_dummy = float(sum(dummy))
    for x in range (len(dummy)):
        dummy[x] /= s_dummy

    s_weights = float(sum(weights))
    for x in range (len(weights)):
        weights[x] /= s_weights

    plt.figure()
    plt.xlabel('Weights []')
    plt.ylabel('Questions []')
    plt.hist(weights,bins=20,log=True)
    plt.savefig('plots/weights.eps')

    #now show sample test from each method
    test1 = np.random.choice(pass_svm,5,p=dummy)
    q_ids = [i[0] for i in stuff]
    test2 = np.random.choice(q_ids,5,p=weights)

    print ' ' 
    print '***********************************************'
    print 'SVM test sample:     ', test1
    print 'Weights test sample: ', test2

run()
