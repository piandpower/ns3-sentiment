import numpy as np
from sklearn.metrics import precision_score
from data_prep import DataPurpose
from dueling_lstms import compute_scale_factor
from dueling_lstms import label_sentences
from dueling_lstms import reload_model
from dueling_lstms import SourceStance
from collections import Counter

def eval_labeled_data():
    # Load training and testing splits
    sentences_training = open('data/training.dat', 'r')
    sentences_testing = open('data/testing.dat', 'r')

    # Load models
    cons_model, cons_vocab = reload_model(SourceStance.conservative)
    lib_model, lib_vocab = reload_model(SourceStance.liberal)

    Y_train = []
    train_predictions = []

    # Label each training sentence
    for line in sentences_training.readlines():
        split = line.split("\t")
        Y_train.append(int(split[1]))
        sentence = split[0]
        label = label_sentence(cons_model, lib_model, cons_vocab, lib_vocab, sentence)
        train_predictions.append(label)

    Y_test = []
    test_predictions = []

    # Label each testing sentence
    # for line in sentences_testing.readlines():
    #     split = line.split("\t")
    #     Y_test.append(int(split[1]))
    #     sentence = split[0]
    #     label = label_sentence(cons_model, lib_model, cons_model, lib_vocab, sentence)
    #     test_predictions.append(label)

    # Calculate the training and testing precision scores
    training_precision = precision_score(Y_train, train_predictions)
    testing_precision = precision_score(Y_test, test_predictions)

    print("Training precision: ", str(training_precision))
    print("Testing precision: ", str(testing_precision))

def eval_predict_provenance(data_purpose):
    # Filenames of testing data
    if (data_purpose == DataPurpose.testing):
        print("using test data")
        cons_file = "data/testing/conservative.dat"
        lib_file = "data/testing/liberal.dat"
        neutral_file = "data/testing/neutral.dat"
    elif (data_purpose == DataPurpose.validation):
        print("using validation data")
        cons_file = "data/valid/conservative.dat"
        lib_file = "data/valid/liberal.dat"
        neutral_file = "data/valid/neutral.dat"

    # Load models
    cons_model, cons_vocab = reload_model(SourceStance.conservative)
    lib_model, lib_vocab = reload_model(SourceStance.liberal)

    scaling_factor = compute_scale_factor(cons_model,lib_model,cons_vocab,lib_vocab)
    lib_thresh = 30
    cons_thresh = 40

    # Label each testing sentence
    print("labeling conservative sentences")
    cons_sentences = open(cons_file).readlines()
    Y_cons_test = np.repeat(-1, len(cons_sentences))
    cons_labels = label_sentences(cons_model,
                                  lib_model,
                                  cons_vocab,
                                  lib_vocab,
                                  cons_sentences,
                                  cons_scale_factor=scaling_factor,
                                  lib_thresh=lib_thresh,
                                  cons_thresh=cons_thresh)

    # Calculate the training and testing precision scores
    cons_testing_precision = precision_score(Y_cons_test, cons_labels, average='micro')
    unique, counts = np.unique(cons_labels, return_counts=True)
    cons_counts = dict(zip(unique, counts))

    # Label each testing sentence
    print("labeling liberal sentences")
    lib_sentences = open(lib_file).readlines()
    Y_lib_test = np.repeat(1, len(lib_sentences))
    lib_labels = label_sentences(cons_model,
                                 lib_model,
                                 cons_vocab,
                                 lib_vocab,
                                 lib_sentences,
                                 cons_scale_factor=scaling_factor,
                                 lib_thresh=lib_thresh,
                                 cons_thresh=cons_thresh)

    lib_testing_precision = precision_score(Y_lib_test, lib_labels, average='micro')
    unique, counts = np.unique(lib_labels, return_counts=True)
    lib_counts = dict(zip(unique, counts))

    print("Conservative testing precision: ", str(cons_testing_precision))
    print("Conservative prediction counts: ", cons_counts)
    print("Liberal testing precision: ", str(lib_testing_precision))
    print("Liberal prediction counts: ", lib_counts)

def main():
    eval_predict_provenance(DataPurpose.validation)

if __name__ == '__main__':
    main()