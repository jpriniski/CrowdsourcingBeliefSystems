"""
Crowdsourcing to analyze belief systems underlying social issues
J. Hunter Priniski and Keith Holyoak

Description:
AnalyzeLanguage.py looks at moral and statistical language use in
Reddit Change My View discussion about capital punishment
"""
from pprint import pprint
import pandas as pd
import csv
import re, string

#we will stem terms in MFD to match with stems from text
from nltk.stem.porter import *
stemmer = PorterStemmer()

def code_word(word, mfd, stats_terms):

    if word.isnumeric():
        return 'STATS', 'NUMERIC'
    elif word in mfd.keys():
        return "MORAL", (word, mfd[word])
    elif word in stats_terms:
        return 'STATS', word
    else:
        if '%' in word or '$' in word:
            return 'STATS', word
        else:
            return "_STOPWORD", None

def main():

    punctuation = re.sub('[$%<=>]', "", string.punctuation)

    mfd_df = pd.read_excel('mfd.xlsx')

    #terms as stems, increases mfd's coverage of terms in corpus
    mfd = {}

    for term, category in mfd_df.values.tolist():
        mfd.update({stemmer.stem(term):category})

    #read in stats_df
    with open('statsdict.txt', 'r') as f:
        stats_dict = [line.rstrip() for line in f]

    data = pd.read_csv('CapPunRedditData_long.csv').dropna(subset=['selftext', 'comment_body'])
    data['selftext'] = data.apply(lambda row: row.selftext.split('\n_____\n\n>', 1)[0], axis = 1)

    #data is long, we are only looking at posts data so we can make remove repeated measures (at comment level)
    data = data.drop_duplicates('postid')

    data_coded = []

    for index, row in data.iterrows():

        text = row[2] + ' ' + row[3]
        #remove punctuation
        text2 = text.translate(str.maketrans('', '', punctuation))

        #make lowercase
        text3 = text2.lower()

        for word in text3.split():
            stem = stemmer.stem(word)
            category, instance = code_word(stem, mfd, stats_dict)
            #caste to list for subsetting ease
            if isinstance(instance, tuple):
                instance = instance[-1]

            data_coded.append([row['postid'], word, category, instance, row['Position']])



    data_long = pd.DataFrame(data_coded, columns = ['postid', 'word', 'category', 'instance','Position'])
    data_long.to_csv('data_coded.csv', index=False)


main()




"""
moral language measured using moral foundations dictionary
Categories
1	care.virtue
2	care.vice
3	fairness.virtue
4	fairness.vice
5	loyalty.virtue
6	loyalty.vice
7	authority.virtue
8	authority.vice
9	sanctity.virtue
10	sanctity.vice
%
"""






#
