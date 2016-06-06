import csv
from readers import *
from predictors import *
from plotters import *

#main code:
trans = read_data_trans('customer_trans_log.csv')
total_spending_plot(trans)
avgs_all = []
demo_types = ['geography','loyalty','email','category','gender','income']

for x in range(1,7):
    demo_x = read_data_demo('customer_info.csv',x)
    avgs_x = avgs(trans,demo_x)
    avg_extrapolation_plots(avgs_x,demo_types[x-1])
    for y in avgs_x:
        avgs_all.append(y)

preds = linear_reg(trans,avgs_all)

with open('out.csv','wb') as out:
    writer = csv.writer(out,delimiter=',')
    writer.writerow(['customer_id','three_month_pred'])
    for x in sorted(preds):
        writer.writerow([x,preds[x]])

