# -*- coding: utf-8 -*-
"""nlp2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sNMFribsW_6reI2LTpzgPXbFnwhQD17I
"""

# install necessary packages using pip
!pip install keras numpy wget

import os
import sys
import numpy

from google.colab import drive
drive.mount('/content/drive')
gdrive_path = '/content/drive/My Drive/'

def load_corpus(path):

    # Check if the path is a directory.
    path = gdrive_path + path
    if not os.path.isdir(path):
        sys.exit("Input path is not a directory")

    # TODO: Your code goes here
    sentences = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:
            for line in f:
                pairs = line.split()
                sentence = []
                for pair in pairs: 
                    tup = pair.split("/")
                    if(len(tup) == 2):
                        sentence.append((tup[0].upper(), tup[1]))
                if len(sentence) > 0:
                    sentences.append(sentence)
    return sentences

path = "modified_brown"
data = load_corpus(path)
print(data[0])

import numpy as np # you may need this to convert lists to np arrays before returning them

wordToIdx = {}
tagToIdx = {}
idxToTag = {}

# Creates the dataset with train_X (words) and train_y (tag).
def create_dataset(sentences):
    # Defines the relevant lists.
    train_X, train_y = list(), list()
    wordToIdx["PAD"] = 0
    wordToIdx["OOV"] = 1
    tagToIdx["PAD"] = 0
    idxToTag[0] = "PAD"
    wordIdx = 2
    tagIdx = 1
    for sentence in sentences:
      curX = []
      cury = []
      for tup in sentence:
        word = tup[0].lower()
        tag = tup[1]
        if word not in wordToIdx:
          wordToIdx[word] = wordIdx
          wordIdx += 1
        if tag not in tagToIdx:
          tagToIdx[tag] = tagIdx
          idxToTag[tagIdx] = tag
          tagIdx += 1
        curX.append(wordToIdx[word])
        cury.append(tagToIdx[tag])
      train_X.append(numpy.array(curX))
      train_y.append(numpy.array(cury))
    return numpy.array(train_X, dtype=object), numpy.array(train_y, dtype=object)

tx, ty = create_dataset(data)
print(tx)
print(ty)

from keras_preprocessing.sequence import pad_sequences as pad

# Pad the sequences with 0s to the max length.
def pad_sequences(train_X, train_y):
    # Use MAX_LENGTH to record length of longest sequence 
    # TODO: Your code goes here
    maxSentences = None
    train_X = pad(train_X, padding="post")
    train_y = pad(train_y, padding="post")
    MAX_LENGTH = len(train_X[0])
    return train_X, train_y, MAX_LENGTH

train_X, train_y, MAX_LENGTH = pad_sequences(tx, ty)
print(train_X, MAX_LENGTH)
print(train_y)

from keras.models import Sequential
from keras.layers import InputLayer, Activation
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed, Embedding
from keras.optimizers import Adam
from keras import activations

# Define the Keras model.
def define_model(MAX_LENGTH):  
    model = Sequential()
    model.add(InputLayer(input_shape=(MAX_LENGTH, )))
    model.add(Embedding(len(wordToIdx), 128))
    model.add(Bidirectional(LSTM(256, return_sequences=True)))
    model.add(TimeDistributed(Dense(len(tagToIdx), activation = 'softmax')))

    model.compile(loss='categorical_crossentropy',
              optimizer=Adam(0.001),
              metrics=['accuracy'])
    
    print (model.summary())
    return model

# Call the function here
model = define_model(MAX_LENGTH)

# Returns the one-hot encoding of the sequence.
from keras.utils import np_utils

def to_categorical(train_y, num_tags = 11):
  cat = np_utils.to_categorical(train_y)
  return cat

# Call the function as to_categorical(train_y, num_tags = len(tag2idx))
tytest = to_categorical(train_y, num_tags = len(tagToIdx))
print(tytest)

import tensorflow as tf

# Trains the model.
def train(model, train_X, train_y):

    # Fit the data into the Keras model, through 40 passes (epochs) using model.fit()
    model.fit(train_X, to_categorical(train_y, len(tagToIdx)), batch_size=128, epochs=40, validation_split=0.2)
 
    # Return the model.
    return model

# call function here
model = train(model, train_X, train_y)

def uncategorize(sequences):
    seq = sequences[0]
    token_sequence = []
    for categorical in seq:
        token_sequence.append(idxToTag[np.argmax(categorical)])
    return token_sequence

def test(model, sample):
  sample = sample.split()
  n = len(sample)
  test_X = []
  snums = []
  for w in sample:
    w = w.lower()
    if w in wordToIdx:
      snums.append(wordToIdx[w])
    else:
      snums.append(wordToIdx["OOV"])
  test_X.append(numpy.array(snums))
  test_X = numpy.array(test_X, dtype=object)
  test_X = pad(test_X, maxlen=MAX_LENGTH, padding="post")
  predictions = model.predict(test_X)
  tagOutput = uncategorize(predictions)
  return tagOutput[:n]

s1 = "the planet jupiter and its moons are in effect a mini solar system ."
s2 = "computers process programs accurately ."

print(s1)
print(test(model, s1))
print(s2)
print(test(model, s2))