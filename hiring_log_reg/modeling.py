import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

'''
To run: python modeling.py data/data_exercise_applicants.csv data/data_exercise_hires.csv plots/
If csv files are in a different place, change appropriate arguments
To send output plots to another directory, change last argument
'''

def fit_and_evaluate(X_train,y_train,X_test,y_test,fit_type):
    reg = linear_model.LogisticRegression()
    fit = reg.fit(X_train,y_train)

    preds = reg.predict(X_test)
    residuals = y_test - preds
    r2 = residuals * residuals
    rss = 0
    for x in r2:
        rss += float(x)

    rss /= float(len(r2))

    #score the result using test data
    result = reg.score(X_test,y_test)
    print 'Normalized rss for %s: %.3f' % (fit_type,rss)
    print 'Score for %s is: %.3f' % (fit_type,result)

    if len(sys.argv) > 3:
    #visualize the resulting probabilities
        probs = reg.predict_proba(X_test)
        p0 = []
        p1 = []
        p2 = []
    
        for x in probs:
            p0.append(x[0])#p(0)
            p1.append(x[1])#p(0)
            p2.append(x[2])#p(0)

        output_string = '%s/probability_%s_comp.png' % (sys.argv[3], fit_type)
        fig1 = plt.figure()
        plt.hist(p2,50,facecolor='red',label='P(case 2)')
        plt.hist(p1,50,facecolor='green',label='P(case 1)')
        plt.hist(p0,50,facecolor='blue',label='P(case 0)')
        plt.xlabel('Regression output probability []')
        plt.ylabel('A.U. []')
        plt.legend()
        plt.savefig(output_string)
        plt.close(fig1)    

if len(sys.argv) < 2:
    print "Please enter the location of your applicant and hire data files"

apps = pd.read_csv(sys.argv[1])
hires = pd.read_csv(sys.argv[2])

#clean up the answers if not filled in
apps['answer1'].fillna(0,inplace=True)
apps['answer2'].fillna(0,inplace=True)
apps['answer3'].fillna(0,inplace=True)
apps['answer4'].fillna(0,inplace=True)
apps['answer5'].fillna(0,inplace=True)
apps['answer6'].fillna(0,inplace=True)
apps['answer7'].fillna(0,inplace=True)
apps['answer8'].fillna(0,inplace=True)
apps['answer9'].fillna(0,inplace=True)
apps['answer10'].fillna(0,inplace=True)
apps['answer11'].fillna(0,inplace=True)
apps['answer12'].fillna(0,inplace=True)
apps['answer13'].fillna(0,inplace=True)
apps['answer14'].fillna(0,inplace=True)
apps['answer15'].fillna(0,inplace=True)
apps['answer16'].fillna(0,inplace=True)
apps['answer17'].fillna(0,inplace=True)
apps['answer18'].fillna(0,inplace=True)
apps['answer19'].fillna(0,inplace=True)
apps['answer20'].fillna(0,inplace=True)
apps['answer21'].fillna(0,inplace=True)
apps['answer22'].fillna(0,inplace=True)
apps['answer23'].fillna(0,inplace=True)
apps['answer24'].fillna(0,inplace=True)
apps['answer25'].fillna(0,inplace=True)
apps['log_total_time'].fillna(0,inplace=True)

#clean up tenure info
hires['tenure_length'].fillna(0,inplace=True)

#add the labels we care about
hires['turnover_6'] = np.where((hires['tenure_length'] < 180) & (hires['currently_employed'] == 'N'), 1, 0)
hires['turnover_12'] = np.where((hires['tenure_length'] > 180) & (hires['tenure_length'] < 360) & (hires['currently_employed'] == 'N'), 1, 0)

apps['client_id1'] = np.where(apps['client_name'] == 'client1',1,0)
apps['client_id2'] = np.where(apps['client_name'] == 'client2',1,0)
apps['client_id3'] = np.where(apps['client_name'] == 'client3',1,0)
apps['client_id4'] = np.where(apps['client_name'] == 'client4',1,0)

hire_dict = {}
for x in range(len(hires['user_id'])):
    status = -1
    if hires['turnover_6'][x] > 0:
        status = 0
    elif hires['turnover_12'][x] > 0:
        status = 1
    else:
        status = 2
    hire_dict[hires['user_id'][x]] = status

#generate data for logistic regression
#labels derived above are the attributes
#answers to questions 1-25 are the features
#also consider individual questions as the single feature
labels = []
answers = []
client = []
time = []

for x in range(len(apps['user_id'])):
    id = apps['user_id'][x]
    if id in hire_dict.keys():
        labels.append(hire_dict[id])
        answers.append([int(apps['answer1'][x]),int(apps['answer2'][x]),int(apps['answer3'][x]),int(apps['answer4'][x]),int(apps['answer5'][x]),
                        int(apps['answer6'][x]),int(apps['answer7'][x]),int(apps['answer8'][x]),int(apps['answer9'][x]),int(apps['answer10'][x]),
                        int(apps['answer11'][x]),int(apps['answer12'][x]),int(apps['answer13'][x]),int(apps['answer14'][x]),int(apps['answer15'][x]),
                        int(apps['answer16'][x]),int(apps['answer17'][x]),int(apps['answer18'][x]),int(apps['answer19'][x]),int(apps['answer20'][x]),
                        int(apps['answer21'][x]),int(apps['answer22'][x]),int(apps['answer23'][x]),int(apps['answer24'][x]),int(apps['answer25'][x])])
        client.append([int(apps['client_id1'][x]),int(apps['client_id2'][x]),int(apps['client_id3'][x]),int(apps['client_id4'][x])])
        time.append([float(apps['log_total_time'][x])])

#split data into train and test samples
np.random.seed(0)
rand_list = np.random.permutation(len(labels))

num_2 = 0
for x in labels:
    if x == 2:
        num_2 += 1.0

X1_train = []
X2_train = []
X3_train = []
y_train = []
for x in range(0,len(rand_list) - 180):
    X1_train.append(answers[rand_list[x]])
    X2_train.append(client[rand_list[x]])
    X3_train.append(time[rand_list[x]])
    y_train.append(labels[rand_list[x]])

X1_test = []
X2_test = []
X3_test = []
y_test = []
for x in range(len(rand_list) - 180,len(rand_list)):
    X1_test.append(answers[rand_list[x]])
    X2_test.append(client[rand_list[x]])
    X3_test.append(time[rand_list[x]])
    y_test.append(labels[rand_list[x]])

#perform logistic regression
print "**************************************"
fit_and_evaluate(X1_train,y_train,X1_test,y_test,'quiz')
fit_and_evaluate(X2_train,y_train,X2_test,y_test,'client')
fit_and_evaluate(X3_train,y_train,X3_test,y_test,'time')
print "**************************************"
print "Random guessing would give: %.3f" % (1.0 / 3.0)
print "Dominant class guess give: %.3f" % (num_2 / float(len(labels)))
