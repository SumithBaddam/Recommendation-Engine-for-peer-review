import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import pandas as pd
from cmath import nan
from audioop import reverse
import csv
import json
from sklearn.model_selection import train_test_split


stemmer = LancasterStemmer()
training_data = []
engg_dat_total = pd.read_csv("EnggRec_data.csv", encoding="ISO-8859-1")

engg_dat, test = train_test_split(engg_dat_total, test_size = 0.2)
a = engg_dat["Unnamed: 0"]
#print(list(engg_dat))
#print(len(engg_dat))
#print(len(test))
#print(engg_dat["Headline"][1])
#for i in range(0,len(engg_dat)):
for i in a:
    i=i-1
    training_data.append({"class": engg_dat["Engineer"][i], "sentence": engg_dat["Headline"][i], "Response": engg_dat["Engineer"][i]})

#print(training_data[1])
#print ("%s sentences of training data" % len(training_data))
# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lower-case each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1
            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
#print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
#print ("Class words: %s" % class_words)

# we can now calculate a score for a new sentence
#sentence = "good day for us to have lunch?"
print("Training is completed.")
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
    
    
#for c in class_words.keys():
#    print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))

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
    #print(score)
    #print(class_name)
    #return float(score/length)
    return score


#for c in class_words.keys():
    #print ("Class: %s  Score: %s \n" % (c, calculate_class_score_commonality(sentence, c)))
    
# return the class with highest score for sentence
def classify(sentence, top_m):
    #high_class = None
    #high_score = 0
    top_classes = []
    high_scores = []
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        #if (score > min(high_scores)):
        #print("YES")
        top_classes.append((c, score))
            #high_scores.append(score)
            #high_class = c
            #high_score = score
    classes = sorted(top_classes, key=lambda x:x[1], reverse=True)
    #print(classes[:10][1])
    names = []
    for k in classes[:top_m]:
        #IF THAT GUY HAS WORKED ON THAT COMPONENT BEFORE, WE 
        names.append(k[0])
    #return high_class, high_score
    #return top_classes, high_scores
    #print(names)
    return names
    
def test_accuracy(test_df, top_m):
    count = 0
    i=0
    for index, row in test_df.iterrows():
        print(i)
        i+=1
        sentence = row["Headline"]
        engineer = row["Engineer"]
        print(sentence)
        print(engineer)
        res = classify(sentence, top_m)
        print(res)
        if(engineer in res):
            count = count + 1
    accuracy = count/len(test_df)
    return accuracy

def main():
    sentence = "DNS and HTTP proxy config not retained after recover app"
#    print(class_words["oalonso"])
    #print(classify(sentence))
    accuracy = test_accuracy(test[:30], 10)
    #pd.DataFrame(class_words.items(), columns=['Engineer', 'Keywords'])
    '''
with open('reviewers_keywords', 'w') as f:
    #data['new_key'] = [1, 2, 3]
    json.dump(class_words, f)

with open('corpus_words', 'w') as f:
    #data['new_key'] = [1, 2, 3]
    json.dump(corpus_words, f)

with open('reviewers_keywords', 'r') as f:
    try:
        class_words = json.load(f)
    # if the file is empty the ValueError will be thrown
    except ValueError:
        class_words = {}
print(class_words["oalonso"])

with open('corpus_words', 'r') as f:
    try:
        corpus_words = json.load(f)
    # if the file is empty the ValueError will be thrown
    except ValueError:
        corpus_words = {}
    
    d = pd.DataFrame()
    for i in class_words.items():
        for key, value in i:
    '''

if __name__ == '__main__':
    main()
