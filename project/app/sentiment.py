import pickle
from nltk.data import load
import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

from .gettweets import get_tweets_search

# from sklearn.model_selection import train_test_split
# from nltk.stem import PorterStemmer
# from nltk.stem import WordNetLemmatizer
# ML Libraries

# from sklearn.metrics import accuracy_score
# from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Global Parameters
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
stop_words = set(stopwords.words('english'))

def preprocess_tweet_text(tweet):
    tweet.lower()
    # Remove urls
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    # Remove user @ references and '#' from tweet
    tweet = re.sub(r'\@\w+|\#','', tweet)
    # Remove punctuations
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    # Remove stopwords
    tweet_tokens = word_tokenize(tweet)
    filtered_words = [w for w in tweet_tokens if not w in stop_words]
    
    # ps = PorterStemmer()
    # stemmed_words = [ps.stem(w) for w in filtered_words]
    # lemmatizer = WordNetLemmatizer()
    # lemma_words = [lemmatizer.lemmatize(w, pos='a') for w in stemmed_words]
    
    return " ".join(filtered_words)

def load_model(filename):
    filename = 'app/model/'+filename
    infile = open(filename, 'rb')
    file = pickle.load(infile)
    infile.close()
    return file

def int_to_string(sentiment):
    if sentiment == 0:
        return "Negative"
    elif sentiment == 2:
        return "Neutral"
    else:
        return "Positive"

def get_sentiment(tweets = get_tweets_search()):
    # tweets = get_tweets_search()
    # tweets = [preprocess_tweet_text(i.text) for i in tweets]

    # vector = pickle.load(open('app/model/vector.pkl', 'rb'))
    vector = load_model('vector')
    # C:\Users\EMMA PRAISE\Documents\Account Audit\tweeter\app\model\vector
    tweet_transform = vector.transform(np.array(tweets).ravel())

    model = load_model('model')
    prediction = model.predict(tweet_transform)
    sentiment = [int_to_string(i) for i in prediction]
    return sentiment

def to_Dataframe(tweets):
    tweets = [preprocess_tweet_text(i.text) for i in tweets]
    sentiment = get_sentiment(tweets)
    data = {'Tweets':tweets, 'Sentiment': sentiment}
    dataframe = pd.DataFrame(data= data)
    dataframe.to_csv('app/export/hello.csv')
    return dataframe


# get_sentiment()