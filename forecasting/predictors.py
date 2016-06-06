import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from datetime import datetime
from readers import *

date_format = "%Y-%m-%d"

def extrapolate(slope,intercept,num_trans,dr1,dr2):
    amt_extra = 0
    for i in range(1000):
        days_extra = (int)(np.random.poisson(num_trans)/3.0)

        #now 'simulate' the next three months
        for mc in range(days_extra):
            x_mc = np.random.uniform(dr1,dr2)
            y_mc = x_mc * slope + intercept
            if y_mc < 0.0:
                y_mc = 0.0
            amt_extra += y_mc
    
    return amt_extra/1000.0

def avgs(trans,demo):
    #do regression over all users with similar demographic data
    avgs = {}

    t0 = datetime.strptime('2014-09-01',date_format)#first day in data set
    ti = datetime.strptime('2015-06-01',date_format)#first day of prediction
    tf = datetime.strptime('2015-08-31',date_format)#last day of prediction

    cases = set()
    for y in demo.keys():
        cases.add(demo[y][0])
 
    list_cases = list(cases)

    dates = []
    amt = []

    for x in list_cases:
        dates.append([])
        amt.append([])

    for y in trans.keys():
        hist = trans[y]
        dem_info = demo[y]

        for z in range(len(list_cases)):
            if list_cases[z] == dem_info[0]:
                for x in hist:
                    t1 = datetime.strptime(x[0],date_format)
                    dates[z].append([(float)((t1 - t0).days)])
                    amt[z].append([x[1]])
    
    values = []

    for z in range(len(list_cases)):
        reg = linear_model.LinearRegression()
        reg.fit(dates[z],amt[z])
        slope = (float)(reg.coef_[0])
        intercept = (float)(reg.intercept_[0])

        values.append([slope,intercept,np.mean(amt[z])])

    return values

def linear_reg(trans,avgs):
    preds = {}
    t0 = datetime.strptime('2014-09-01',date_format)#first day in data set
    ti = datetime.strptime('2015-06-01',date_format)#first day of prediction
    tf = datetime.strptime('2015-08-31',date_format)#last day of prediction
    
    for y in trans.keys():
        hist = trans[y]
        dates = []
        amt = []

        for x in hist:
            t1 = datetime.strptime(x[0],date_format)
            dates.append([(float)((t1 - t0).days + 1)])
            amt.append([x[1]])
            
        if len(hist) >= 6:
            #if the user has enough transactions for a good regression, just use their own data
            reg = linear_model.LinearRegression()
            reg.fit(dates,amt)
            slope = (float)(reg.coef_[0])
            intercept = (float)(reg.intercept_[0])

            preds[y] = extrapolate((float)(reg.coef_[0]),(float)(reg.intercept_[0]),len(dates),(ti-t0).days,(tf-t0).days)

            #just for visual reference
            if len(hist) > 35:
                x_res = np.arange(0,(tf-t0).days,1)
                y_res = slope * x_res + intercept

                fig = plt.figure()
                plt.scatter(dates,amt,color='black',label='Data')
                plt.plot(x_res,y_res,color='blue',linewidth=3,label='Linear fit')
                plt.ylim(0,60)
                plt.xlim(0,365)
                plt.vlines((ti-t0).days,0,150,color='red',linewidth=1,label='Date of extrapolation')
                plt.xlabel('Days [since start of data set]',fontsize=10)
                plt.ylabel('Transaction amount [USD]',fontsize=10)
                this_title = 'Linear regression for customer %d' % y
                plt.title(this_title)
                plt.legend(fontsize=10)
                
                name = 'plots/fit_%d_%d.png' % (len(hist), y)
                plt.savefig(name)
                plt.close(fig)
        else: 
            #if the user does not have enough transactions for a good regression, use averages from other users with similar demographics
            closest = -1
            diff = 100000
            this_mean = np.mean(amt)

            #for now, we define 'similarity' by comparing the user's average transaction to the average from all demographic groups
            for z in range(len(avgs)):
                if np.absolute(avgs[z][2] - this_mean) < diff:
                    closest = z
                    diff = np.absolute(avgs[z][2] -this_mean)

            preds[y] = extrapolate(avgs[closest][0],avgs[closest][1],len(dates),(ti-t0).days,(tf-t0).days)

    return preds
