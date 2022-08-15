import requests
from datetime import datetime
from datetime import timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json, re, traceback

# install Vader Sentiment Package
#pip install vaderSentiment

SENTIMENT_POSITIVE = 'POSITIVE'
SENTIMENT_NEGATIVE = 'NEGATIVE'
SENTIMENT_NEUTRAL = 'NEUTRAL'

class SentimentAnalyser:
       # Initialise - set API KEY
       def __init__(self):
              self.api_key = None # set api key

       # function to analyse single sentiment
       def get_sentiments(self, sentence):
       
              # Create a SentimentIntensityAnalyzer object.
              sid_obj = SentimentIntensityAnalyzer()
              
              # polarity_scores method of SentimentIntensityAnalyzer
              # object gives a sentiment dictionary.
              # which contains pos, neg, neu, and compound scores.
              sentiment_dict = sid_obj.polarity_scores(sentence)
              
              #print("Overall sentiment dictionary is : ", sentiment_dict)
              #print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
              #print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
              #print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
              
              #print("Sentence Overall Rated As", end = " ")
              
              # decide sentiment as positive, negative and neutral
              if sentiment_dict['compound'] >= 0.05 :
                     return SENTIMENT_POSITIVE
              
              elif sentiment_dict['compound'] <= - 0.05 :
                     return SENTIMENT_NEGATIVE
              
              else :
                     return SENTIMENT_NEUTRAL

       # sanitise words
       def sanitise_words(self, words):
              words_to_remove=['private', 'limited', 'pvt.', 'ltd.']
              sanitised_words = list()
              for word in words:
                     for w_remove in words_to_remove:
                            w_sanitised = re.compile(w_remove, re.IGNORECASE).sub("", word).strip()
                            sanitised_words.append(w_sanitised)
              
              all_words = words + sanitised_words # add all possible words
              all_words = list(set(all_words)) # remove duplicates, if any
              
              return  all_words

       # analyse sentiments - default timeframe is 10 days
       def analyse_sentiments(self, stock_symbol, company_name, industry, timeframe=10):
              
              sentiment_result = SENTIMENT_NEUTRAL
              try:
                     # since last 2 days
                     date = (datetime.now() - timedelta(days=timeframe)).strftime("%Y-%m-%d")
                     # prepare words with company name and stock symbol
                     words = self.sanitise_words([company_name, stock_symbol])
                     # sanitise industry names
                     industry = industry.replace("&","")

                     word_string='"{0}"'.format(words[0])
                     if len(words) > 1:
                            word_string = "("+word_string # start parenthesis
                            for i in range(1, len(words)):
                                   word_string = word_string+' OR "{}"'.format(words[i])
                            word_string = word_string+")" # close parenthesis
                     word_string = word_string+' AND ("Share" OR "Stock" OR "{}")'.format(industry)
                     url = ('https://newsapi.org/v2/everything?'
                            'q={}&'
                            'from={}&'
                            'language=en&'
                            'sort_by=relevancy&'
                            'apiKey={}'.format(word_string, date, self.api_key))
                     
                     response = requests.get(url)
                     data = json.loads(response.content)
                     #print(data)
                     if len(data['articles']) > 1: # if data is found
                            data['articles'].sort(key=lambda x: x['publishedAt'], reverse=True) # sort by date
                            sentences = [i['description'] for i in data['articles'] if word_string for w in words if w in i['description']]
                            sentences = list(set(sentences)) # remove duplicates
                            
                            if len(sentences) > 1: # if sentences are more than 1
                                   sentiments = [self.get_sentiments(s) for s in sentences]
                                   pos_sentiments = len([s for s in sentiments if s == SENTIMENT_POSITIVE])
                                   neg_sentiments = len([s for s in sentiments if s == SENTIMENT_NEGATIVE])
                                   #print("Positive:"+str(pos_sentiments))
                                   #print("Negative:"+str(neg_sentiments))
                                   if pos_sentiments > neg_sentiments:
                                          sentiment_result = SENTIMENT_POSITIVE
                                   elif neg_sentiments > pos_sentiments:
                                          sentiment_result = SENTIMENT_NEGATIVE
              except Exception:
                     print(traceback.format_exc())
                     pass
              
              return sentiment_result

# Execution
obj = SentimentAnalyser()
print(obj.get_sentiments("Sachin Tendulkar is not a great player"))

# sentiment analysis of stocks from News API - https://newsapi.org
#print(obj.analyse_sentiments("INFY", "Infosys", "IT"))