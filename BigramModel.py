from sys import argv, stdout
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from numpy.random import choice, rand


class myarray(np.ndarray):
    def __new__(cls, *args, **kwargs):
        return np.array(*args, **kwargs).view(myarray)
    def index(self, value):
        return np.where(self == value)


class badBigramModel:
    def __init__(self, punctuation):
        self.punctuation = punctuation

    def fit(self, str):
        def stringToList(string, punct):
            wordList = string.split()
            i = 0
            for word in wordList:
                if word in punct:
                    wordList.pop(i)
                elif word[-1] in punct:
                    wordList[i] = word[:-1]
                    word = wordList[i]
                elif word[0] in punct:
                    wordList[i] = word[1:]
                i += 1
            return wordList

        words = stringToList(str, self.punctuation)
        uniqwords = set(words)
        listunicwords = list(uniqwords)
        nparray = np.array(words)

        model = {}

        for word in uniqwords:
            a = myarray(nparray)
            index = a.index(word)
            indexnext = tuple(np.array(index) + np.ones((len(index)), dtype=np.int8))
            if word == words[len(words)-1]:
                model[word] = [choice(list(uniqwords))]
                continue
            model[word] = nparray[indexnext]
            status = int((100*(listunicwords.index(word)))/len(listunicwords))
            stdout.write("\r%d%% %s" % (status, word))
            stdout.flush()

        self.model = model
        self.words = words

    def predict(self, textlenth):
        outstring = ""
        upword = ""
        for i in range(textlenth):
            if i == 0:
                upword = choice(self.words)
                outstring += upword + ' '
            else:
                upword = choice(self.model[upword])
                outstring += upword + ' '
            status = int((100*i)/textlenth)
            stdout.write("\r%d%% %s" % (status, upword))
            stdout.flush()
        print()
        return outstring




class goodBigramModel:
    def __init__(self, n_grams=4):
        self.n_grams = n_grams
        self.vectorizer = CountVectorizer (ngram_range=(1,self.n_grams))


    def fit(self, string):
        data = ['']
        data[0] = string

        counts = self.vectorizer.fit_transform(data)
        counts = np.array(counts.sum(axis=0))[0]

        feature_names = self.vectorizer.get_feature_names()

        self.continuations = {}

        for ngram, count in zip(feature_names, counts):
            words = ngram.split()
            prv = ' '.join(words[:-1])
            nxt = words[-1]
            if prv not in self.continuations:
                self.continuations[prv] = {}
            self.continuations[prv][nxt] = count


    def predict(self, length):
        text = ''

        for j in range(length):
            for i in range(-(self.n_grams-1), -1):
                cur_prefix = ' '.join(text.split()[i:])
                if cur_prefix not in self.continuations:
                    continue
                options = list(self.continuations[cur_prefix].items())
                words = [option[0] for option in options]

                probilities = np.array([option[1] for option in options])
                probilities = probilities / probilities.sum()

                prob = rand()
                k = 0
                while prob > probilities[k]:
                    prob -= probilities[k]
                    k += 1

                text += ' ' + words[k]
                break

        return text
