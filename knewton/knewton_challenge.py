import csv
import sys
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.cluster import KMeans
from sklearn import svm

def run_numpy():
    f = np.genfromtxt('astudentData.csv',delimiter=',',skip_header=1,dtype=(float,float,float))
    
    id_frac = []#store pairs of question id (dummy!) and fraction of right answers
    id = []
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
            id_frac.append([sum_response,sum_correct / sum_response])
            id.append(sum_response)
            frac.append(sum_correct / sum_response)
            sum_correct = ans
            sum_response = 1
            counter += 1#unique, incremental identifier of question ID
        q_last = q_id #increment last question ID number
        entries += 1 #probably a better way to do this

#    plt.hist2d(id,frac,[25,25])
#    plt.savefig('plots/frac_vs_id.eps')

#    t_svm = svm.LinearSVC(random_state=0)
    t_svm = svm.SVC(random_state=0,kernel='linear')

#    t_svm = sklearn.cluster.KMeans(n_clusters=3)

    target = []
    t_data = []

    random.seed(1)

    tx1 = []
    ty1 = []

    tx2 = []
    ty2 = []

    tx3 = []
    ty3 = []

    tx4 = []
    ty4 = []

    tx5 = []
    ty5 = []

    tx6 = []
    ty6 = []

    for x in range(200):
        target.append(0)
        t_data.append([random.uniform(2500,3500),random.uniform(0.55,0.65)])
        tx1.append(random.uniform(2500,3500))
        ty1.append(random.uniform(0.55,0.65))

        target.append(1)
        t_data.append([random.uniform(0,2500),random.uniform(0.35,0.85)])
        tx2.append(random.uniform(0,2500))
        ty2.append(random.uniform(0.35,0.85))

        target.append(2)
        t_data.append([random.uniform(0,3500),random.uniform(0.0,0.35)])
        tx3.append(random.uniform(0,3500))
        ty3.append(random.uniform(0.0,0.35))

        target.append(3)
        t_data.append([random.uniform(0,3500),random.uniform(0.85,1.0)])
        tx4.append(random.uniform(0,3500))
        ty4.append(random.uniform(0.85,1.0))

        target.append(4)
        t_data.append([random.uniform(2500,3500),random.uniform(0.65,0.85)])
        tx5.append(random.uniform(2500,3500))
        ty5.append(random.uniform(0.65,0.85))

        target.append(5)
        t_data.append([random.uniform(2500,3500),random.uniform(0.35,0.55)])
        tx6.append(random.uniform(2500,3500))
        ty6.append(random.uniform(0.35,0.55))

    plt.figure()
    plt.plot(tx1,ty1,'go',tx2,ty2,'go',tx3,ty3,'ro',tx4,ty4,'ro',tx5,ty5,'ro',tx6,ty6,'ro')
    plt.savefig('plots/test_data.eps')

    t_svm.fit(t_data,target)
    res = t_svm.predict(id_frac)

    id_pass = []
    frac_pass = []

    id_fail = []
    frac_fail = []

    for x in range (len(res)):
        if res[x] == 0 or res[x] == 1:
            id_pass.append(id[x])
            frac_pass.append(frac[x])
        else:
            id_fail.append(id[x])
            frac_fail.append(frac[x])
#        if res[x] == 2:
#            id_fail2.append(id[x])
#            frac_fail2.append(frac[x])

    print len(id_pass), len(id_fail)

#    plt.axis([0,4000,0,1])
    plt.figure()
    plt.plot(id_fail,frac_fail,'ro',id_pass,frac_pass,'go')
#    plt.plot(id_pass,id_fail,"ro")
    plt.savefig('plots/frac_vs_num_scatter.eps')
    #plt.hist2d(id_fail,frac_fail,[100,100],[(0,4000),(0,1)],False,None,1)
    #plt.savefig('plots/frac_vs_num_fail.eps')

    #plt.figure()
    #plt.hist2d(id_pass,frac_pass,[100,100],[(0,4000),(0,1)],False,None,1)
    #plt.savefig('plots/frac_vs_num_pass.eps')
    

#    print res

#    plt.axis([0,400,-0.5,1.5])
#    plt.plot(res,'bo')
#    plt.savefig('plots/res_svm.eps')

def run_panda():
    f = pd.read_csv('astudentData.csv')

    all_wrong = float(len(f[f.correct == 0]))
    all_right = float(len(f[f.correct == 1]))

    all_avg = all_right / (all_wrong + all_right)

    q_sig = f.groupby('question_id').var()['correct']
    q_avg = f.groupby('question_id').mean()['correct']

    print q_avg

    final = np.exp(-1.0 * abs(q_avg - all_avg) / q_sig)

#    for x in final:
#        print x

run_numpy()

#    q_sig.hist()
#    plt.savefig('plots/question_sig.eps')
