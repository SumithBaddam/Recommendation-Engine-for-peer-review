import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import pandas as pd
from cmath import nan
from audioop import reverse
import csv
import json
from sklearn.model_selection import train_test_split

with open('reviewers_keywords', 'r') as f:
    try:
        class_words = json.load(f)
    # if the file is empty the ValueError will be thrown
    except ValueError:
        class_words = {}

with open('corpus_words', 'r') as f:
    try:
        corpus_words = json.load(f)
    # if the file is empty the ValueError will be thrown
    except ValueError:
        corpus_words = {}

stemmer = LancasterStemmer()

# calculate a score for a given class
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with same weight
            score += 1            
            if show_details:
                print ("   match: %s" % stemmer.stem(word.lower() ))
    return score
    
    
# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    length = 0
    for word in nltk.word_tokenize(sentence):
        length+=1
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / float(corpus_words[stemmer.stem(word.lower())]))
            #score += 1
            #print(corpus_words[stemmer.stem(word.lower())])
            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / float(corpus_words[stemmer.stem(word.lower())])))
    
    #return float(score/length)
    return score
    
    
# return the class with highest score for sentence
def classify(sentence, top_m):
    top_classes = []
    high_scores = []
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        top_classes.append((c, score))    
    classes = sorted(top_classes, key=lambda x:x[1], reverse=True)
    names = []
    for k in classes[:top_m]:
        names.append(k[0])
    return names
    

def test_accuracy(test_df, top_m):
    count = 0
    i=0
    for index, row in test_df.iterrows():
        print(i)
        i+=1
        sentence = row["Headline"]
        engineer = row["Engineer"]
        res = classify(sentence, top_m)
        if(engineer in res):
            count = count + 1
    accuracy = count/len(test_df)
    return accuracy


def main():
    #engg_dat_total = pd.read_csv("EnggRec_data.csv", encoding="ISO-8859-1")
    #engg_dat, test = train_test_split(engg_dat_total, test_size = 0.2)
    #accuracy = test_accuracy(test[:30], 10)
