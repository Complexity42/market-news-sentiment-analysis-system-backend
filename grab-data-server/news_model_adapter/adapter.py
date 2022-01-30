from nltk.sentiment.vader import SentimentIntensityAnalyzer

from util.summarization import getExtractiveSummarization

def toOutput(input):

    # print(input)

    # sentiment_score #
    analyzer = SentimentIntensityAnalyzer().polarity_scores(input['content'])
    positive = analyzer['pos']
    negative = analyzer['neg']
    score = positive - negative
    input['sentiment_score'] = score
    
    # summary #
    summary = getExtractiveSummarization(input['content'])
    input['summary'] = summary

    return input




