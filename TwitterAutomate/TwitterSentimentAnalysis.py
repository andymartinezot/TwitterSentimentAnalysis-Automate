import tweepy
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime
from textblob import TextBlob
from fpdf import FPDF
from pdfreport import create_report, create_title
from datetime import timedelta
from AutomateMail import send_mail

##------------Creating function to obtain percentage------------
def percentage(part, whole):
    return 100 * float(part)/float(whole)

##------------Generating your keys for the access---------------

consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_toke'
access_token_secret = 'your_access_token_secret'

##----------Creating variables for the use of the date---------

current_date_and_time = datetime.datetime.now().strftime("_%Y%m%d-%H:%M")
current_date_and_time_string = str(current_date_and_time)

##----------Authenticate with Twitter--------------------------
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
#Create variable to use API and authenticate
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

##------------Creating the inputs (Word and number of words to search)-----------

searchTearm = input('Enter Keyword/Hashtag to search: ')
numberOfSearch = int(input('Enter the number of tweets to analayze: '))

##-----------Creating the list of tweets to analyse-----------------------------

tweets = tweepy.Cursor(api.search, q=searchTearm, tweet_mode='extended').items(numberOfSearch)

##----------Creating variables to evaluate the sentiments-----------------------

positive = 0
negative = 0
neutral = 0
polarity = 0

##-----------Creating the .txt file----------------------------

header = ['user','tweet','sentiment','date']
f= open("/home/andy/Documents/PythonExercises/TwitterAutomate/TweetsAnalized.csv","w+",encoding='UTF8')
f.write("User|Tweet|Sentiment|Date|Location" + '\n')

##-----------Evaluating tweet by tweet-------------------------

for tweet in tweets:
    #Loop to check if the tweet is a retweet. This is made to obtain the complete full text of a retweet
    if 'retweeted_status' in tweet._json:
        analysis_row = tweet._json['retweeted_status']['full_text']#Getting retweet
    else:
        analysis_row = tweet._json['full_text']#Getting tweet
    
    analysis_row = TextBlob(analysis_row)#Using library to evaluate the sentiment of the tweet
    user_row = tweet.user.screen_name#Get username
    time_row = tweet._json['created_at']#Get date of tweet
    location_row = tweet._json['user']['location']
    if location_row == "":
        location_row = "There is no location"
    else:
        location_row = location_row

    language = analysis_row.detect_language()#Detecting language of the tweet

    #Loop to check if the tweet is wrote in English
    if language == 'en':
        analysis = analysis_row.replace('|','')
    else:
        analysis = analysis_row.translate(to='en').replace('|','')

    polarity += analysis.sentiment.polarity#Obtaining polarity value
    
    #Populating the counters and saving the .csv file
    if (analysis.sentiment.polarity == 0):
        neutral += 1
        f.write( str(user_row) + "|" + str(analysis) + '|NEUTRAL' + '|Created: ' + str(time_row) + '|Location: ' + str(location_row) + '\n')
    elif (analysis.sentiment.polarity > 0.00):
        positive += 1
        f.write( str(user_row) + "|" + str(analysis) + '|POSITIVE' + '|Created: ' + str(time_row) + '|Location: ' + str(location_row) + '\n')
    elif (analysis.sentiment.polarity < 0.00):
        negative += 1
        f.write( str(user_row) + "|" + str(analysis) + '|NEGATIVE' + '|Created: ' + str(time_row) + '|Location: ' + str(location_row) + '\n')

f.close()#Closing the .txt file

positive = percentage(positive, numberOfSearch)#Positive percentage
negative = percentage(negative, numberOfSearch)#Negative percentage
neutral = percentage(neutral, numberOfSearch)#neutral percentage
polarity = percentage(polarity, numberOfSearch)#polarity percentage

#Formating the percentage, ie: 7.00
positive = format(positive, '.2f')
negative = format(negative, '.2f')
neutral = format(neutral, '.2f')

##------------------Printing in console how the people is reacting to the tweets.-----------------
print("How people are reacting on " + searchTearm + " by analyzing " + str(numberOfSearch) + " Tweets.")

if (polarity == 0):
    print("Neutral")
elif (polarity < 0.00):
    print ("Negative")
elif (polarity > 0.00):
    print("Positive")

##Creating the graph and saving it.
labels = ['Positive ['+str(positive)+'%]', 
          'Neutral ['+str(neutral)+'%]', 
          'Negative ['+str(negative)+'%]']
sizes = [positive, neutral, negative]
n = len(labels)
colors = plt.cm.Oranges(np.linspace(0.35,0.65,n))
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting on " + searchTearm + " by analyzing " + str(numberOfSearch) + " Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.savefig("/home/andy/Documents/PythonExercises/TwitterAutomate/TweetsAnalized.png")

##Create Report

width = 210
height = 297
pdf=FPDF()

day = datetime.datetime.now().strftime("%m/%d/%y")
create_report(day)

##Send Email

EMAIL_ADDRESS = "andytesting361@gmail.com"
EMAIL_PASSWORD = "your_password"

send_mail(EMAIL_ADDRESS, EMAIL_PASSWORD)
