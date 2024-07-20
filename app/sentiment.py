from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

analyzer = SentimentIntensityAnalyzer()

def getVaderSentiment(sentence):
    score = analyzer.polarity_scores(sentence)
    print("{:-<65} {} {}".format(sentence, '(v)', str(score['compound'])))
    return score['compound'] 

def getBlobSentiment(sentence):
    blob = TextBlob(sentence)
    polarity = blob.sentiment.polarity
    print("{:-<65} {} {}".format(sentence, '(b)', str(polarity)))
    return polarity


def main():
    teststrs = ['This is not useful']
    for teststr in teststrs:
        getVaderSentiment(teststr)
        getBlobSentiment(teststr)

if __name__ == "__main__":
    main()