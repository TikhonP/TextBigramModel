from sys import argv, stdout
from collections import Counter
import numpy as np
from random import choice


class myarray(np.ndarray):
    def __new__(cls, *args, **kwargs):
        return np.array(*args, **kwargs).view(myarray)
    def index(self, value):
        return np.where(self == value)


class bigramModel:
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


print('\n----------------------------\nTikhonSystems\n----------------------------')
print('\nЗапуск\n')

script, filename, textlenth = argv
textlenth = int(textlenth)

print('Открытие файла ...\n')
str = ((open(filename)).read()).lower()
punctuation = ['.',',',':',';','!','?','(',')', '-', '--', '\"', '{', '}']

print('Инициализация модели ...\n')
textGenerator = bigramModel(punctuation)

print('Обучение модели ...')
textGenerator.fit(str)

print('\n\nГенерация текста ...')
predictedString = textGenerator.predict(textlenth)

print('\nЗапись сгенерированного текста в файл ...\n')
outputfile = open('output.txt', 'w')
outputfile.write(predictedString)
outputfile.close()

print('Сгенерированный текст:\n')
print(predictedString, '\n')
