import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import pandas as pd
from cmath import nan
from audioop import reverse
import csv
import json
from sklearn.model_selection import train_test_split

from django.db import models
from dataServices.db import DbConn
from constance import config

class EngRecTesting(models.Model):

	with open('/auto/vgapps-cstg02-vapps/analytics/csap/ingestion/scripts/engTxtRecc/reviewers_keywords', 'r') as f:
		try:
			class_words = json.load(f)
		# if the file is empty the ValueError will be thrown
		except ValueError:
			class_words = {}

	with open('/auto/vgapps-cstg02-vapps/analytics/csap/ingestion/scripts/engTxtRecc/corpus_words', 'r') as f:
		try:
			corpus_words = json.load(f)
		# if the file is empty the ValueError will be thrown
		except ValueError:
			corpus_words = {}

	stemmer = LancasterStemmer()

	# calculate a score for a given class
	@staticmethod
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
	@staticmethod
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
	@staticmethod
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

'''    
def main():
	sentence = "DNS and HTTP proxy config not retained after recover app"
	top_m = 10
	classify(sentence, top_m)
'''
