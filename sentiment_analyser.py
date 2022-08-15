# install Vader Sentiment Package
#pip install vaderSentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Class to implement Sentiment Analysis Logic
class SentimentAnalyser:
       
       # function to analyse single sentiment
       def get_sentiments(self, sentence):
       
              # Create a SentimentIntensityAnalyzer object.
              sid_obj = SentimentIntensityAnalyzer()

              # polarity_scores method of SentimentIntensityAnalyzer
              # object gives a sentiment dictionary.
              # which contains pos, neg, neu, and compound scores.
              sentiment_dict = sid_obj.polarity_scores(sentence)

              #print("Overall sentiment dictionary is : ", sentiment_dict)
              print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
              print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
              print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
              print("sentence was rated as ", sentiment_dict['compound']*100, "% Compound Rating")

              # # decide sentiment as positive, negative and neutral
              if sentiment_dict['compound'] >= 0.05 :
                     print("Overall Sentiment is: Positive")

              elif sentiment_dict['compound'] <= - 0.05 :
                     print("Overall Sentiment is: Negative")

              else :
                     print("Overall Sentiment is: Neutral")      


# Execution
sentence = "Sachin Tendulkar is a great player"
obj = SentimentAnalyser()
obj.get_sentiments(sentence)