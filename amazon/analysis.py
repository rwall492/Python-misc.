import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

keywords = 50

def makeSeries(documents):
    count = CountVectorizer(stop_words = 'english')
    word_count = count.fit_transform(documents)
    words = count.get_feature_names()

    v_data = []
    v_words = []

    total = 0.

    for n in word_count[0].indices:
        total += word_count[0,n]

    for n in word_count[0].indices:
        v_data.append([word_count[0,n],words[n]])
        v_words.append(words[n])

    series = pd.Series(v_data,v_words)
    return series

def makeSentimentVector(documents):
    count = CountVectorizer(stop_words = 'english')#as written, this shouldn't matter, right?
    word_count = count.fit_transform(documents)
    words = count.get_feature_names()

    v_count = []
    v_words = []

    for n in word_count[0].indices:
        v_count.append(word_count[0,n])
        v_words.append(words[n])

    vec_words = pd.Series(v_count,v_words)

    science = 0
    animal = 0
    emotion = 0
    machine = 0

    s_words = ['science','future','progress','hope','concern','worry']
    a_words = ['dog','cat','animal','pig','monkey','rat','cow','horse','chickens','hens']
    e_words = ['passion','romance','attraction','lust','desire','excitement','love','hate','contempt','hatred']
    m_words = ['car','truck','van','tractor','airplane','jet','tank','bomber','fighter','taxi']

    for x in s_words:
        try:
            science += vec_words[x]
        except:
            science += 0
    for x in a_words:
        try:
            animal += vec_words[x]
        except:
            animal += 0
    for x in e_words:
        try:
            emotion += vec_words[x]
        except:
            emotion += 0
    for x in m_words:
        try:
            machine += vec_words[x]
        except:
            machine += 0

    norm = float(machine + science + animal + emotion)

    vec = [float(science)/norm,float(animal)/norm, float(emotion)/norm, float(machine)/norm]
    return vec

def processFile(filename):
    documents = []
    file = open(filename,'r')
    documents.append(file.read().replace('\n',' ').replace('\r',' '))

    series = makeSeries(documents)
    series.sort(ascending=False)
    
    summary = []
    for x in range(0,keywords):
        summary.append(series[x][1])

    vector = makeSentimentVector(documents)
        
    output = [vector, summary]
    return output

titles = ['1984','bnw','chicken','ender','farm','gatsby','giver','herriot','mockingbird','rebecca']
books = []

for x in titles:
    temp = processFile('review_data/reviews_%s.txt' % x)
    books.append(temp)

sim = []

for j in range(0,10):
    shared = []
    for x in range(0,10):
        total = 0
        for y in books[j][1]:
            word = y
            for z in books[x][1]:
                new_word = z
                if y == z:
                    total += 1.0
        shared.append(total/float(keywords))
    sim.append(shared)

plt.figure(1)
plt.title('Fraction of shared key words')
plt.xlabel('Book []',fontsize=10)
plt.ylabel('Book []',fontsize=10)
plt.imshow(sim)
plt.colorbar()
plt.savefig('plots/similarity.png')

plt.figure(2)
plt.subplot(221)
labels = ['Science','Animal','Emotion','Machine']
colors = ['red','yellow','green','blue']
plt.title('1984')
plt.pie(books[0][0],labels=labels,colors=colors)
plt.subplot(222)
labels = ['Science','Animal','Emotion','Machine']
colors = ['red','yellow','green','blue']
plt.title('Brave New World')
plt.pie(books[1][0],colors=colors)
plt.subplot(223)
labels = ['Science','Animal','Emotion','Machine']
colors = ['red','yellow','green','blue']
plt.title('Animal Farm')
plt.pie(books[4][0],colors=colors)
plt.subplot(224)
labels = ['Science','Animal','Emotion','Machine']
colors = ['red','yellow','green','blue']
plt.title('Rebecca')
plt.pie(books[9][0],colors=colors)
plt.savefig('plots/piechart.png')
