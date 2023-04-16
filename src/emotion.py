
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
from nltk.corpus import stopwords
def sentiment_score(msg):
    print(msg)

    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(msg)
    print(ss)

    pos = ss['pos']
    neg = ss['neg']
    neu = ss['neu']

    if neg>pos:
        p=5-(neg*5)
        if p>2.5:
            return p-2.5
        else :
            return p
    else:
        if pos==0.0:
            pos=.35
        p=5*pos
        if p<3.5:
            p=p+1.5
        return p

# print(sentiment_score("work completed as expected"))