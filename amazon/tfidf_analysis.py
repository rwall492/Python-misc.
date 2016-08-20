import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def make_series(documents):
    count = TfidfVectorizer()
    word_count = count.fit_transform(documents)
    words = count.get_feature_names()
    print word_count

def processFile(filename):
    documents = []
    file = open(filename,'r')
    documents.append(file.read().replace('\n',' ').replace('\r',' '))

    series = make_series(documents)
    '''
    summary = []
    for x in range(0,keywords):
        summary.append(series[x][1])

    vector = makeSentimentVector(documents)
        
    output = [vector, summary]
    return output
    '''

titles = ['1984','bnw','chicken','ender','farm','gatsby','giver','herriot','mockingbird','rebecca']
books = []

#for x in titles:
#temp = processFile('review_data/reviews_%s.txt' % x)
temp = processFile('review_data/reviews_1984.txt')
    #books.append(temp)
