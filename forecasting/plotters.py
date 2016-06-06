import matplotlib.pyplot as plt
import numpy as np

def total_spending_plot(trans):

    values = []
    counts = []

    for x in trans:
        amt = 0
        hist = trans[x]
        for y in hist:
            amt += (float)(y[1])
        values.append(amt)
        counts.append(len(hist))

    fig = plt.figure()
    plt.hist(values,100)
    plt.xlabel('Transaction total [USD]')
    plt.ylabel('Customers []')
    plt.title('Transaction total for each customer in database')
    plt.xlim(0,900)
    plt.savefig('plots/total_spending.png')
    plt.close(fig)

    fig = plt.figure()
    plt.hist(counts,40)
    plt.xlabel('Total number of transactions []')
    plt.ylabel('Customers []')
    plt.title('Number of transactions for each customer in database')
    plt.xlim(0.5,45.5)
    plt.savefig('plots/total_counts.png')
    plt.close(fig)

def avg_extrapolation_plots(avgs,type):
    fig = plt.figure()

    labels = []
    this_title = ''
    if type == 'geography':
        labels = ['"F"', '"G"', '"J"', '"D"', '"E"', '"H"', '"I"', '"B"', '"C"', '"A"']
        this_title = 'Geographic region'
    if type == 'loyalty':
        labels = [0, 1]
        this_title = 'Loyalty card'
    if type == 'email':
        labels = [0, 1]
        this_title = 'Email campaign'
    if type == 'category':
        labels = ['"M"', '"P"', '"Q"', '"N"', '"O"', '"L"']
        this_title = 'Favorite topic'
    if type == 'gender':
        labels = ['"M"', '"F"']
        this_title = 'Gender'
    if type == 'income':
        labels = [1, 2, 3]
        this_title = 'Income Level'

    for x in range(len(avgs)):
        x_res = np.arange(0,365,1)
        y_res = avgs[x][0] * x_res + avgs[x][1]
        blue_val = 1.0 - ((float)(x) / (float)(len(avgs)))
        red_val = 1.0 - blue_val
        plt.plot(x_res,y_res,color=[red_val,0,blue_val],linewidth=3,label=labels[x])

    plt.xlim(0,365)
    plt.ylim(10.5,12.5)
    plt.xlabel('Days [since start of data set]',fontsize=10)
    plt.ylabel('Transaction amount [USD]',fontsize=10)
    plt.title(this_title)
    plt.legend(fontsize=10)
    
    name = 'plots/avg_extrapolation_%s.png' % (type)
    plt.savefig(name)
    plt.close(fig)
