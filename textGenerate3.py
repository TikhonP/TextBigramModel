from BigramModel import badBigramModel, goodBigramModel
from sys import argv

print('\n----------------------------\nTikhonSystems\n----------------------------')
print('\nStarting ...\n')

script, filename, textlenth = argv
textlenth = int(textlenth)

print('File opening ...\n')
strr = str(((open(filename)).read()).lower())

model = input('Do you want to use optimized or hand-written model? Please enter 1 or 2 > ')

if model == '1':
    print('Model initialization ...\n')
    textGenerator = goodBigramModel()

    print('Model fitting ...')
    textGenerator.fit(strr)

    i=0

    def gen(textength):
        print('\n\nText generation ...')
        predictedString = textGenerator.predict(textlenth)
        print('Generated text:\n')
        print((predictedString), '\n')
        if input('Do you want to save it in file? (y/n) > ')=='y':
            name = input('Please enter filename > ')
            print('\nWriting genereted text to file ...\n')
            outputfile = open(name+'.txt', 'w')
            outputfile.write(name+'.txt')
            outputfile.close()

    while True:
        if i!=0:
            if input('Do you want to generate new text? (y/n) > ')=='y':
                textlenth = int(input('Please input text length > '))
                gen(textlenth)
            else:
                break
        else:
            gen(textlenth)
            i=1

else:
    punctuation = ['.',',',':',';','!','?','(',')', '-', '--', '"', '{', '}']

    print('Model initialization ...\n')
    textGenerator = badBigramModel(punctuation)

    print('Model fitting ...')
    textGenerator.fit(strr)

    i=0

    def gen(textength):
        print('\n\nText generation ...')
        predictedString = textGenerator.predict(textlenth)
        print('Generated text:\n')
        print((predictedString), '\n')
        if input('Do you want to save it in file? (y/n) > ')=='y':
            name = input('Please enter filename > ')
            print('\nWriting genereted text to file ...\n')
            outputfile = open(name+'.txt', 'w')
            outputfile.write(name+'.txt')
            outputfile.close()

    while True:
        if i!=0:
            if input('Do you want to generate new text? (y/n) > ')=='y':
                textlenth = int(input('Please input text length > '))
                gen(textlenth)
            else:
                break
        else:
            gen(textlenth)
            i=1

print('\nStopping working...')
