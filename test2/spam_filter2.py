# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:59:30 2019

@author: SKsaqlain
"""

import os
import re
import string
import math
import json
import pickle
from sklearn.model_selection import train_test_split
from sklearn import feature_extraction, model_selection, naive_bayes, metrics, svm

DATA_DIR = 'enron'
target_names = ['ham', 'spam']
 
def get_data(DATA_DIR):
	#THE TRAINING DATA IS SKEWED TOWARDS ONE SIDE.
	# subfolders = ['enron%d' % i for i in range(1,4)] #15% 
	# subfolders = ['enron%d' % i for i in range(4,7)] #100%
	subfolders = ['enron%d' % i for i in range(4,7)]
 
	data = []
	target = []
	for subfolder in subfolders:
		# spam
		spam_files = os.listdir(os.path.join(DATA_DIR, subfolder, 'spam'))
		for spam_file in spam_files:
			with open(os.path.join(DATA_DIR, subfolder, 'spam', spam_file), encoding="latin-1") as f:
				data.append(f.read())
				target.append(1)
 
		# ham
		ham_files = os.listdir(os.path.join(DATA_DIR, subfolder, 'ham'))
		for ham_file in ham_files:
			with open(os.path.join(DATA_DIR, subfolder, 'ham', ham_file), encoding="latin-1") as f:
				data.append(f.read())
				target.append(0)
 
	return data, target

class SpamDetector(object):
    """Implementation of Naive Bayes for binary classification"""
    def clean(self, s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)
 
    def tokenize(self, text):
        text = self.clean(text).lower()
        return re.split("\W+", text)
 
    def get_word_counts(self, words):
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0.0) + 1.0
        return word_counts
    
    def fit(self, X, Y):
        self.num_messages = {}
        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = set()
     
        n = len(X)
        self.num_messages['spam'] = sum(1 for label in Y if label == 1)
        self.num_messages['ham'] = sum(1 for label in Y if label == 0)
        # self.log_class_priors['spam'] = math.log(self.num_messages['spam'] / n)
        # self.log_class_priors['ham'] = math.log(self.num_messages['ham'] / n)
        self.log_class_priors['spam'] = math.log(self.num_messages['spam'] / n)
        self.log_class_priors['ham'] = math.log(self.num_messages['ham'] / n)
        self.word_counts['spam'] = {}
        self.word_counts['ham'] = {}
     
        for x, y in zip(X, Y):
            c = 'spam' if y == 1 else 'ham'
            counts = self.get_word_counts(self.tokenize(x))
            for word, count in counts.items():
                if word not in self.vocab:
                    self.vocab.add(word)
                if word not in self.word_counts[c]:
                    self.word_counts[c][word] = 0.0
     
                self.word_counts[c][word] += count
       
            
    def predict(self, X):
        result = []
        for x in X:
            counts = self.get_word_counts(self.tokenize(x))
            spam_score = 0
            ham_score = 0
            for word, _ in counts.items():
                if word not in self.vocab: continue
                
                # add Laplace smoothing
                #with log 93%
                #with add-2 93%
                #with add-3 93%
                log_w_given_spam = math.log( (self.word_counts['spam'].get(word, 0.0)+3) / (self.num_messages['spam'] + len(self.vocab)) )
                log_w_given_ham = math.log( (self.word_counts['ham'].get(word, 0.0)+3) / (self.num_messages['ham'] + len(self.vocab)) )

                #9% accuracy
                # log_w_given_spam = (self.word_counts['spam'].get(word, 0.0) + 3) / (self.num_messages['spam'] + len(self.vocab)) 
                # log_w_given_ham = (self.word_counts['ham'].get(word, 0.0) + 3) / (self.num_messages['ham'] + len(self.vocab))
	    			

                spam_score += log_w_given_spam
                ham_score += log_w_given_ham
	     
            spam_score += self.log_class_priors['spam']
            ham_score += self.log_class_priors['ham']
     
            if spam_score > ham_score:
                result.append(1)
            else:
                result.append(0)
        return result




#SVM gave 79% accuracy on test data
#f = feature_extraction.text.CountVectorizer(stop_words = 'english')
#X_transformed= f.fit_transform(X)
#
#X_train,X_test,y_train,y_test=train_test_split(X_transformed,y,test_size=0.3,random_state=42)
#
#
#svc = svm.SVC(C=2)
#svc.fit(X_train, y_train)
#
#print(svc.score(X_test, y_test))


#MNB gave 83% accuracy.
if __name__=="__main__":
    X, y = get_data(".")
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
    MNB = SpamDetector()
    MNB.fit(X_train, y_train)
    #saving the model
    with open("model.pckl","wb") as m:
        pickle.dump(MNB,m)  
    pred = MNB.predict([data])
    true = y_test
    accuracy = sum(1 for i in range(len(pred)) if pred[i] == true[i]) / float(len(pred))
    print("{0:.4f}".format(accuracy))
    

def predict(data):
    with open("model.pckl","rb") as m:
        MNB2=pickle.load(m)
        print(MNB2)
    return(MNB2.predict(data))
    