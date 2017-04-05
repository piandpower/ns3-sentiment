from gensim.models import Word2Vec
from nltk import pos_tag
from nltk import word_tokenize
import numpy as np
from article_utils import read_data_file

word2vec_filepath = "./data/GoogleNews-vectors-negative300.bin"

# word2vec similarity between the topic and the nouns of the candidate sentence
def nouns_sim(word2vec, sentences, tagged_sentences, tagged_topic):
    sim_scores = np.zeros((len(sentences)))
    for i, tagged_sentence in enumerate(tagged_sentences):
        topic_nouns = {word for word, pos in tagged_topic
                       if pos.startswith("NN") and word in word2vec.vocab}
        sentence_nouns = {word for word, pos in tagged_sentence
                          if pos.startswith("NN") and word in word2vec.vocab}
        if len(sentence_nouns) == 0 or len(topic_nouns) == 0:
            sim_scores[i] = 0
            continue
        similarity = word2vec.n_similarity(topic_nouns, sentence_nouns)
        print "topic nouns are: ", topic_nouns
        print "sentence nouns are: ", sentence_nouns
        print "similarity is: ", similarity
        sim_scores[i] = similarity
    return sim_scores

def compute_sim(sentences, topic, word2vec):
    print "sentences are: ", sentences
    tagged_sentences = [pos_tag(word_tokenize(sentence)) for sentence in sentences]
    tagged_topic = pos_tag(word_tokenize(topic))
    return nouns_sim(word2vec, sentences, tagged_sentences, tagged_topic)

def load_word2vec():
    print("loading word2vec")
    word2vec = Word2Vec.load_word2vec_format(word2vec_filepath, binary=True)
    print("finished loading word2vec")
    return word2vec