#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Models.FeatureProcessing import *
import sklearn
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import abc
from ClassificationModule import ClassificationModule



def myTokenizer(s):
    """Needed for CountVectorizer"""
    return s.split(' ')

class allmultinomialnb(ClassificationModule):
    """A basic SVC"""

    def __init__(self, text_corpus, filetype_corpus, filename_corpus, foldername_corpus):
        ClassificationModule.__init__(self, "All Multinomial NB", "A Multinomial Naive Bayes-Classifier used with all data")

        # Create vectorizer and fit on all available Corpi
        self.vectorizer = getTextVectorizer(6000) # Maximum of different columns
        self.filetypeVectorizer = getTextVectorizer(30) 
        self.foldernameVectorizer = getTextVectorizer(100)
        self.filenameVectorizer = getTextVectorizer(200) 

        # Vectorizer for descriptions and/or readmes
        corpus = []
        for text in text_corpus:
            corpus.append(process_text(text))
        self.vectorizer.fit(corpus)

        # Vectorizer for filetypes
        corpus = []
        for type in filetype_corpus:
            corpus.append(type)
        self.filetypeVectorizer.fit(corpus)

        # Vectorizer for filenames
        corpus = []
        for type in filename_corpus:
            corpus.append(type)
        self.filenameVectorizer.fit(corpus)

        # Vectorizer for foldernames
        corpus = []
        for folder in foldername_corpus:
            corpus.append(folder)
        self.foldernameVectorizer.fit(corpus)

        # Create classifier
        self.clf = MultinomialNB()
        
        print "\t-", self.name


    def resetAllTraining(self):
        """Reset classification module to status before training"""
        self.clf = sklearn.base.clone(self.clf)

    def trainOnSample(self, sample, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird."""
        vec = self.formatInputData(sample)
        label_index = getLabelIndex(sample)
        return self.clf.fit(vec, np.expand_dims(label_index, axis=0))

    def train(self, samples, nb_epoch=10, shuffle=True, verbose=True):
        """Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)"""
        train_samples = []
        train_lables = []
        for sample in samples:
            formatted_sample = self.formatInputData(sample)[0].tolist()
            train_samples.append(formatted_sample)
            train_lables.append(getLabelIndex(sample))
        train_lables = np.asarray(train_lables)
        train_result = self.clf.fit(train_samples, train_lables)
        self.isTrained = True
        return train_result


    def predictLabel(self, sample):
        """Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde"""
        if not self.isTrained:
            return 0
        sample = self.formatInputData(sample)
        return self.clf.predict(sample)[0]
    
    def predictLabelAndProbability(self, sample):
        """Return the probability the module assignes each label"""
        if not self.isTrained:
            return [0, 0, 0, 0, 0, 0, 0, 0]
        sample = self.formatInputData(sample)
        prediction = self.clf.predict_proba(sample)[0]
        return [np.argmax(prediction)] + list(prediction) 

    def formatInputData(self, sample):
        """Extract description and transform to vector"""
        sd = getDescription(sample)
        rm = getReadme(sample)
        arr = list(self.vectorizer.transform([sd, rm]).toarray()[0])
        arr += getMetadataVector(sample)
        arr += list(self.filetypeVectorizer.transform([getFiletypesString(sample)]).toarray()[0])
        arr += list(self.foldernameVectorizer.transform([getFoldernames(sample)]).toarray()[0])
        arr += list(self.filenameVectorizer.transform([getFilenames(sample)]).toarray()[0])
        return np.asarray([arr])


