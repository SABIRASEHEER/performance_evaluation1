import numpy as np, pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, accuracy_score


# sns.set() # use seaborn plotting style


import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# for removing repetition from positive and negative words
fulllist=[]
positive = open("positive.txt", "r+")
file = positive.read()
positive_list = []
positive_list = file.split("\n")
df_pos = []
for r in positive_list:
    if r not in df_pos:
        df_pos.append(r)
    if r not in fulllist:
        fulllist.append(r)

positive.close()




negative = open("negative.txt", "r+")
file = negative.read()
negative_list = []
negative_list = file.split("\n")
df_neg = []
for r in negative_list:
    if r not in df_neg:
        df_neg.append(r)
    if r not in fulllist:
        fulllist.append(r)
negative.close()

i = 0
corp = []
tcorp=[]
f_t_label = []
tlabel=[]
listcount = []
count = 0
for rr in df_pos:

#giving label as 0 for positive
    if str(rr) != 'nan':
        corp.append(rr)
        f_t_label.append(0)
        count = count + 1
        if count==10:
            count=0
            tcorp.append(rr)
            tlabel.append(0)

    listcount.append(count)
    i = i + 1
count = 0
for rr in df_neg:


#giving label as 1 for negative
    if str(rr) != 'nan':
        corp.append(rr)
        f_t_label.append(1)
        count = count + 1
        if count==10:
            count=0
            tcorp.append(rr)
            tlabel.append(0)
    listcount.append(count)



vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corp)
print(len(vectorizer.get_feature_names()))
print(vectorizer.get_feature_names())

print(X.toarray())


# Load the dataset
# data = fetch_20newsgroups()# Get the text categories
text_categories = [0,1]#data.target_names# define the training set
train_data =corp #fetch_20newsgroups(subset="train", categories=text_categories)# define the test set
# test_data = fetch_20newsgroups(subset="test", categories=text_categories)



print("We have {} unique classes".format(len(text_categories)))
print("We have {} training samples".format(len(train_data)))
# print("We have {} test samples".format(len(test_data.data)))



# Build the model
model = make_pipeline(TfidfVectorizer(), MultinomialNB())# Train the model using the training data
model.fit(train_data, f_t_label)# Predict the categories of the test data
predicted_categories = model.predict(tcorp)

count=0
for i in range(0,len(tlabel)):
    if predicted_categories[i]==tlabel[i]:
        count=count+1
# print(count,len(tlabel))
# accuracy=(count/len(tlabel))*100
# print(accuracy)



# print(np.array(test_data.target_names)[predicted_categories])
#
#
# # plot the confusion matrix
# mat = confusion_matrix(test_data.target, predicted_categories)
# sns.heatmap(mat.T, square = True, annot=True, fmt = "d", xticklabels=train_data.target_names,yticklabels=train_data.target_names)
# plt.xlabel("true labels")
# plt.ylabel("predicted label")
# plt.show()


# print("The accuracy is {}".format(accuracy_score(train_data, predicted_categories)))


# _____________________________________________________________________________
import nltk
import re
nltk.download('punkt')
import collections
import string
from nltk.tokenize import sent_tokenize,word_tokenize
# str = input("Enter any string: ").lower()
def predict_senti(str):
    str=str.lower()
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~|`'''
    sentences=[str] #sent_tokenize(str)
    new_words = []
    freq_table = {}
    score = {}
    #tokenized_word=[]
    with open("input_data.txt","w+",encoding="UTF-8") as f:
        for sent in sentences:
            new_words = []
            freq_table = {}
            sent = ''.join([i for i in sent if not i.isdigit()])
            for x in sent:
                if x in punctuations:
                    sent = sent.replace(x, "")
            print(sent)
            tokenized_word=word_tokenize(sent)
            print(tokenized_word)
            f.write('\n'.join(tokenized_word)+'\n')



    sent=open("input_data.txt","r+")

    file=sent.read()

    negative_list = file.split("\n")
    df_neg=[]
    for r in negative_list:
        if r not in df_neg:
            if r!='':
                if r in fulllist:
                    df_neg.append(r)

    if len(df_neg)>0:
        print("df negative")
        predicted_categories = model.predict(df_neg)

        print(len(predicted_categories))
        res=((len(predicted_categories)-sum(predicted_categories))/len(predicted_categories))*100
        out="Positive "
        if res<50:
            out="Negative "
            res=100-res
        print("The input is a",out,"sentence with probability of",res,"%")
        r=res*5/100
        if out=="Negative":
            r=5-r
        return [out,r]
    else:
        print("The input is a", "Neutral", "sentence ")
        return "Neutral",2.5
