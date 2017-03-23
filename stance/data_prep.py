import glob
import json
import nltk
import os
from enum import Enum
from typing import Tuple, List

# Filenames to write training data
cons_train_file = "data/training/conservative.dat"
lib_train_file = "data/training/liberal.dat"

# Filenames to write testing data
cons_test_file = "data/testing/conservative.dat"
lib_test_file = "data/testing/liberal.dat"
neutral_test_file = "data/testing/neutral.dat"

# Filenames to write validation data
cons_valid_file = "data/valid/conservative.dat"
lib_valid_file = "data/valid/liberal.dat"

# Conservative or liberal model types for loading data
class DataPurpose(Enum):
    training = 1
    testing = 2
    validation = 3

def fetch_articles(data_purpose):
    # type: (DataPurpose) -> List[Tuple[str,str]]
    if (data_purpose == DataPurpose.training):
        datapattern = 'data/raw/570*/*.json'
    elif (data_purpose == DataPurpose.testing):
        datapattern = 'data/raw/test*/*.json'
    elif (data_purpose == DataPurpose.validation):
        datapattern = 'data/raw/valid*/*.json'
    data = glob.glob(datapattern)
    articles = []
    for i in range(len(data)):
        dataFile = open(data[i], 'r')
        contents = json.load(dataFile)
        site = contents['thread']['site']
        text = contents['text']
        articles.append((site, text))

    return articles



# Given the name of an article folder (conservative, liberal, or neutral) read the 
# articles from that folder and split them into sentences in a file of that name.
# Writes the sentences to liberal and conservative data files
def write_to_files(data_purpose):
    # type: (DataPurpose) -> ()
    articles = fetch_articles(data_purpose)

    if data_purpose == DataPurpose.training:
        os.makedirs("training", exist_ok=True)
        conservative_file = open(cons_train_file, 'w+')
        liberal_file = open(lib_train_file, 'w+')
    elif data_purpose == DataPurpose.testing:
        os.makedirs("testing", exist_ok=True)
        conservative_file = open(cons_test_file, 'w+')
        liberal_file = open(lib_test_file, 'w+')
    elif data_purpose == DataPurpose.validation:
        os.makedirs("valid", exist_ok=True)
        conservative_file = open(cons_valid_file,'w+')
        liberal_file = open(lib_valid_file, 'w+')
    else:
        print("invalid data purpose, exiting")
        return

    for article in articles:
        text = article[1].replace('\n', ' ')
        text = text.replace('\t', ' ')
        source = article[0]

        # Load NLTK sentence tokenizer
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_detector.tokenize(text)

        for sentence in sentences:
            # Right now sourceId 5 is the only conservative source
            if source == "thehill.com" or source == "foxnews.com":
                conservative_file.write(sentence.strip() + os.linesep)
            else:
                liberal_file.write(sentence.strip() + os.linesep)

#TODO: write neutral data

# Given the name of an article folder (conservative, liberal, or neutral) read the
# articles from that folder and split them into sentences in a file of that name.
# Writes the sentences to liberal and conservative data files
def create_combined_data(data_purpose):
    articles = fetch_articles(data_purpose)

    # TODO: rename
    training_file = open('data/training.dat', 'w+')

    for article in articles:
        text = article[1].replace('\n', ' ')
        text = text.replace('\t', ' ')
        source = article[0]

        # Load NLTK sentence tokenizer
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_detector.tokenize(text)

        for sentence in sentences:
            if source == "thehill.com" or source == "foxnews.com":
                training_file.write(sentence.encode('utf-8').strip() + "\t-1" + os.linesep)
            else:
                training_file.write(sentence.encode('utf-8').strip() + "\t1" + os.linesep)

def main():
    write_to_files(DataPurpose.training)
    write_to_files(DataPurpose.testing)
    write_to_files(DataPurpose.validation)

if __name__ == '__main__':
    main()
