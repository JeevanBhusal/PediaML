from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy


def extract_features(words):
    return dict([(word, True) for word in words])

import nltk
nltk.download('movie_reviews')

def SentimentAnalyzer(text):
    # load movie reviews from sample data
    fileids_pos = movie_reviews.fileids('pos')
    fileids_neg = movie_reviews.fileids('neg')

    features_pos = [(extract_features(movie_reviews.words(fileids=[f])),'Positive') for f in fileids_pos]
    features_neg = [(extract_features(movie_reviews.words(fileids=[f])),'Negative') for f in fileids_neg]

    threshold = 1
    num_pos = int(threshold*len(features_pos))
    num_neg = int(threshold*len(features_neg))
    # print(num_pos)
    # print('negative',len(num_neg))

    # creating training and testing data
    features_train = features_pos[:num_pos] + features_neg[:num_neg]
    features_test = features_pos[num_pos:] + features_neg[num_neg:]

    print('\nNumber of training datapoints:', len(features_train))
    print('Number of test datapoints:', len(features_test))

    # training a naive bayes classifier 
    classifier = NaiveBayesClassifier.train(features_train)
    print('Accuracy:',nltk_accuracy(classifier, features_test))

    probabilities = classifier.prob_classify(extract_features(text.split()))
    print(probabilities)
    # Pick the maximum value
    predicted_sentiment = probabilities.max()
    print("Predicted sentiment:", predicted_sentiment)
    return round(probabilities.prob(predicted_sentiment), 2)

    # return predicted_sentiment  
# SentimentAnalyzer('It was not that good.')