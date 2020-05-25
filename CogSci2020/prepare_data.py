"""
Crowdsourcing to analyze belief systems underlying social issues
Prepare Reuters data for spaCy processing and model fitting 
J. Hunter Priniski and Keith Holyoak
"""
import re
import os

#data prep method tailored for Reuters dataset
def prep(data):
    #remove URLs
    data2 = re.sub(r'http\S+', '', data)

    #extract text
    split = data2.split('--')
    text = split[-1]

    #remove location, date info
    text2 = text.split('(Reuters)')[-1]

    #remove unnecessary white space
    text3 = ' '.join(text2.split())

    return text3

path = 'financial-news-dataset-master/TextFiles/'
dfpath = 'financial-news-dataset-master/dataset.txt'

for file in os.listdir(path):

    with open(path + file, 'r') as f:
        data = f.read()
    data_preped = prep(data)

    with open(dfpath, 'a') as f:
        print('writing ', file)
        f.write(data_preped + "\n")
