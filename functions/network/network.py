import warnings
import pickle
import joblib
from nltk.tokenize import sent_tokenize

def netConnect():
    folder = 'functions/network/'
    warnings.filterwarnings('ignore')
    tfidf_transformer = pickle.load(open(folder + 'tfidf.pickle', 'rb'))
    count_vect = pickle.load(open(folder + 'count_vect.pickle', 'rb'))
    clf = joblib.load(folder + 'network.joblib')
    arr = pickle.load(open(folder + 'array_of_answers.pickle', 'rb'))
    return(clf, arr)

def netAnswer(text):
    clf, arr = netConnect()
    # docs = ['Что такое класс?', 'Члены класса - это?', 'Члены класа?']
    docs = sent_tokenize(text)
    predicted = clf.predict(docs)
    worker = []
    for doc, category in zip(docs, predicted):
        worker.append(arr[category].capitalize() + '.')
        print('%r => %s' % (doc, arr[category]))
    return(('\n').join(worker))

# print(netAnswer('Что такое класс? Члены класса - это?'))