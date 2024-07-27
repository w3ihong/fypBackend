from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

analyzer = SentimentIntensityAnalyzer()

def getVaderSentiment(sentence):
    score = analyzer.polarity_scores(sentence)
    return score['compound'] 

def getBlobSentiment(sentence):
    blob = TextBlob(sentence)
    polarity = blob.sentiment.polarity
    return polarity


def main():
    teststrs = ['This is not useful']
    for teststr in teststrs:
        getVaderSentiment(teststr)
        getBlobSentiment(teststr)

if __name__ == "__main__":
    main()