import tweepy
import json
import string
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
#from tkinter import *
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

#from flask import Flask
#app = Flask(__name__)
neg = 0
pos = 0
#root = Tk()

#words = Label(root, text="")
#words.grid()

consumer_key = 'zUYxglUSaANwbQEnZ0CkCpofh'
consumer_secret = 'BHU3ozG5ZBhNz9OuoT9wlEpH8IXokwqPTpHDTKx5UXcZ85GBhu'
access_token = '2722863244-GSQ3JjFVWXoQcWy2YVAY8y4J3H7RewbPzZsNitn'
access_secret = '3gT6SSvXLHUU9Ac8iMt2ykL7K5vn6TIuOi6XUj3Zk8S9o'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
arrayOfData = []
api = tweepy.API(auth)

def word_feats(words):
    return dict([(word, True) for word in words])
 
positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)' ]
negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ,"shit", "fuck", "cunt", "bitch", "arse", "bollocks", "dick", "cock", "bastard"]
neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not' ]

f = open('unigrams-neg.txt', 'r')
f = f.read()
f = f.split(" ")
g = open('unigrams-pos.txt', 'r')
g = g.read()
g = g.split(" ")

positive_features = [(word_feats(pos), 'pos') for pos in g]
negative_features = [(word_feats(neg), 'neg') for neg in f]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
 
train_set = negative_features + positive_features + neutral_features
 
classifier = NaiveBayesClassifier.train(train_set) 
classResult = ""

classResult = ""
timesTried = 0
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                #f.write(data)
                global neg
                global pos
                global timesTried
                global words
                global classResult
                arrayOfData.append(json.loads(data))
                newData = json.loads(data)
                sentence = newData["text"]
                words = sentence.split(" ")
                classResult = classifier.classify(word_feats(words))
                for word in words:
                    #print(classResult)
                    if classResult == "neg":
                        neg += 1
                    elif classResult == "pos":
                        pos += 1
                    else:
                        pass
                #print("Positivity: " + str(pos))
                #print("Negativity: " + str(neg))
                if timesTried == 500:
                    print("Wholesome tweets: " + str(pos))
                    print("Bit of a dickhead tweets: " + str(neg))
                    return False
                else:
                    timesTried += 1
                    #print(timesTried)
                #print(newData['text'])
                #for curseWord in ["shit", "fuck", "cunt", "bitch", "arse", "bollocks", "dick", "cock", "bastard"]:
                    #if curseWord in newData['text']:
                        #print (newData['text'])
                        ##words["text"] = newData["text"]
                        #print(curseWord)
                    #else:
                        #pass
                return True
        except BaseException as e:
            #print("Error on_data: %s" % str(e))
            pass
        return True
 
    def on_error(self, status):
        print(status)
        return True
##root.mainloop()
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(locations=[-180,-90,180,90])
total = pos + neg
print("The world's overall wholesomeness is sitting at " + str(round((pos/total)*100,1)) + "% and the world's overall 'bit of a dickheadedness' is sitting at " + str(round((neg/total)*100,1)) + "%")

