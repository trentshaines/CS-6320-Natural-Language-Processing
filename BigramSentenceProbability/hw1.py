import sys

def printBigramCounts(tokenList):
    pad = max(len(word) for word in tokenList)
    n = len(tokenList)
    sentenceBigramCounts = [[0]*n for i in range(n)]
    for i in range(n):
        for j in range(n):
            sentenceBigramCounts[i][j] = bigramCounts.get((tokenList[i], tokenList[j]), 0)
    headerRow = "".join(word.ljust(pad+1) for word in tokenList)
    print(" "*(pad+1) + headerRow)
    if addOne == 1:
        for i in range(n):
            rowString = "".join(str(count+1).ljust(pad+1) for count in sentenceBigramCounts[i])
            print(tokenList[i].ljust(pad+1) + rowString)
    else:
        for i in range(n):
            rowString = "".join(str(count).ljust(pad+1) for count in sentenceBigramCounts[i])
            print(tokenList[i].ljust(pad+1) + rowString)


def printBigramProbabilities(tokenList):
    n = len(tokenList)
    pad = max(len(word) for word in tokenList)
    sentenceBigramProbability = [[0]*n for i in range(n)]
    for i in range(n):
        for j in range(n):
            sentenceBigramProbability[i][j] = bigramProbability.get((tokenList[i], tokenList[j]), 0)
    headerRow = "".join(word.ljust(pad+1) for word in tokenList)
    print(" "*(pad+1) + headerRow)
    for i in range(n):
        rowString = "".join("{:.{pad}f}".format(count, pad=pad-3).ljust(pad+1) for count in sentenceBigramProbability[i])
        print(tokenList[i].ljust(pad+1) + rowString)


def printSentenceProbability(tokens):
    totalProb = 1
    for i in range(len(tokens)):
        key = ()
        if i == 0:
            key = ("<s>", tokens[0])
        else:
            key = (tokens[i-1], tokens[i])
        prob = bigramProbability.get(key, 0)
        #print(key, prob)
        totalProb *= prob
    print(totalProb)


s1 = "mark antony , heere take you caesars body : you shall not come to them poet ."
s2 = "no , sir , there are no comets seen , the heauens speede thee in thine enterprize ."
tokens1 = list(filter(lambda x: x.isalnum(), s1.split()))
tokens2 = list(filter(lambda x: x.isalnum(), s2.split()))
tokenList1 = list({x for x in tokens1})
tokenList2 = list({x for x in tokens2})
corpusFile = sys.argv[1]
addOne = int(sys.argv[2])
corpus = open(corpusFile)
corpusLines = corpus.readlines()
numLines = len(corpusLines)

unigramCounts = dict()
unigramCounts["<s>"] = numLines

for line in corpusLines:
	words = list(filter(lambda x: x.isalnum(), line.split()))
	for word in words:
		if word in unigramCounts:
			unigramCounts[word] += 1
		else:
			unigramCounts[word] = 1
vocabSize = len(unigramCounts)

bigramCounts = {}
for line in corpusLines:
    words = list(filter(lambda x: x.isalnum(), line.split()))
    for i in range(len(words)):
        key = ()
        if i == 0:
            key = ("<s>",words[0])
        else:
            key = (words[i-1], words[i])
        
        if key in bigramCounts:
            bigramCounts[key] += 1
        else:
            bigramCounts[key] = 1

bigramProbability = {}
for word1 in unigramCounts:
    for word2 in unigramCounts:
        key = (word1, word2)
        wordCount1 = unigramCounts[word1]
        biCount = bigramCounts.get(key, 0)
        if addOne == 1:
            bigramProbability[key] = (biCount+1)/(wordCount1+vocabSize)
        else:
            bigramProbability[key] = biCount/wordCount1

if(addOne == 1):
    print("Currently Training using Add One Smoothing")
else:
    print("Currently Training without smoothing")

#1
print("\nBigram Counts for Sentence 1:")
printBigramCounts(tokenList1)

print("\nBigram Counts for Sentence 2:")
printBigramCounts(tokenList2)

#2
print("\nBigram Probabilities for Sentence 1:")
printBigramProbabilities(tokenList1)
print("\nBigram Probabilities for Sentence 2:")
printBigramProbabilities(tokenList2)

#3
print("\nTotal Sentence Probability for Sentence 1:")
printSentenceProbability(tokens1)
print("\nTotal Sentence Probability for Sentence 2:")
printSentenceProbability(tokens2)

while(True):
    query = input("\nWhat bigram probability do you want to know? Enter \'word1 word2\' for the probability of word2 given word 1: ")
    words = query.split(" ")
    tup = ()
    if(len(words) == 2):
        tup = (words[0], words[1])
    print("The probability of \'" + words[1] + "\' given \'" + words[0] + "\' is: " + str(bigramProbability.get(tup, 0)))