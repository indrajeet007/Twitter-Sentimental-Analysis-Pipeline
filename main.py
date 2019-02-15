#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import packages
import sys
import csv
import tweepy
import matplotlib.pyplot as plt

from collections import Counter
from aylienapiclient import textapi


# In[2]:


# in case running code on python2.7 and lower
if sys.version_info[0] < 3:
    input = raw_input


# In[3]:


# Twitter credintials
consumer_key = "sRPC4AzVXZ7dPYG9Jf2SAWcj4"
consumer_secret = "A2qhpn5REn8broeDRW3CbgQ7aeecJ71wFuukJRmbgVrD9urVT8"
access_token = "3032895760-IsNnchFNj0DhATTkWrXssLhKiwVlT7FGv90lCwu"
access_token_secret = "g5pagQ3xl1QisrXxORIoSJltgvseO70yBc1d54uTKjLya"


# In[4]:


# AYLIEN credintials
app_id = "af0efd19"
app_key = "0134a3b117b5759d2272e9d574cea60f"


# In[5]:


# initialise instance of Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# In[6]:


# initialise instance of AYLIEN
client = textapi.Client(app_id, app_key)


# In[7]:


# testing part
# input a query to test the code
query = input("Subject name to analyze:\n")


# In[8]:


# input number of tweets to analyze
number = input("Number of tweets to analyze?\n")


# In[9]:


# build result search config
results = api.search(
    lang = "en",
    q = query + " -rt",
    count = number,
    result_type = "mixed" # changeable
)

print("--- Gathered Tweets \n")


# In[10]:


# open a csv file to store the scraped tweets and their sentiment output
file_name = 'Sentiment_Analysis_of_{}_Tweets_About_{}.csv'.format(number, query)


# In[11]:


with open(file_name, 'w', newline='') as csvfile:
    csv_writer = csv.DictWriter(
        f = csvfile,
        fieldnames = ["Tweet", "Sentiment", "Confidence"]
    )
    csv_writer.writeheader()
    
    print("--- Opened a CSV file to store the results of your analysis")
    
    # clean tweets and forward to AYLIEN Text API
    for c, result in enumerate(results, start=1):
        tweet = result.text
        tidy_tweet = tweet.strip().encode('ascii', 'ignore')

        if len(tweet) == 0:
            print("Empty Tweet")
            continue

        response = client.Sentiment({'text': tidy_tweet})
        csv_writer.writerow({
            'Tweet': response['text'],
            'Sentiment': response['polarity'],
            'Confidence': response['polarity_confidence']
        })

        print("Analyzed Tweet {}".format(c))


# In[12]:


# count the data in the sentiment column of the CSV file
with open(file_name, 'r') as data:
    counter = Counter()
    
    for row in csv.DictReader(data):
        counter[row['Sentiment']] += 1
        
    positive = counter['positive']
    negative = counter['negative']
    neutral = counter['neutral']


# In[13]:


# declare variables to display a pie chart of outcome sizes using counter variables
colors = ['green', 'red', 'grey']
sizes = [positive, negative, neutral]
labels = 'Positive', 'Negative', 'Neutral'


# In[14]:


# use matplotlib to plot the chart
plt.pie(
    x = sizes,
    shadow = True,
    colors = colors,
    labels = labels,
    startangle = 90
)

plt.title("Sentiment of {} Tweets about {}".format(number, query))
plt.show()

