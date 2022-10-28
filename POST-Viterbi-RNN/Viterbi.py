import os
import sys
#import numpy as np

full_path = os.path.realpath(__file__)
workingDir = os.path.dirname(full_path) + "/"

def load_corpus(path):
    """ Load corpus from a folder / directory
    
    Arg:
        path: a text sequence denotes the path of corpus

    Return:
        sentences: a list of sentences that are preprocessed in the corpus
    """
    sentences = []
    for filename in os.listdir(workingDir+path):
        with open(os.path.join(workingDir+path, filename), 'r') as f:
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
    
class HMMTagger:

    def __init__(self):
        """ Define variables that are used in the whole class

        You shuold initial all variables that are necessary and will be used
        globally in this class, such as the initial probability.
        """
        self.initialCounts = {}
        self.transitionCounts = {}
        self.emissionCounts = {}
        self.tagCounts = {}

        self.sentences = 0
        self.words = set()
        self.tags = set()

        self.initialProbabilities = {}
        self.transitionProbabilities = {}
        self.emissionProbabilities = {}

    def initialize_probabilities(self, sentences):
        """ Initialize / learn probabilities from the corpus

        In this function, you should learn inital probability, transition
        probability, and emission probability. Also, you should apply the
        add-one smoothing properly here.

        Arg:
            sentences: a list of sentences that are preprocessed in the corpus
        """
        for sentence in sentences:
            for i in range(len(sentence)):
                curWord = sentence[i][0]
                curTag = sentence[i][1]
                self.tagCounts[curTag] = self.tagCounts.get(curTag, 0)+1

                self.words.add(curWord)
                self.tags.add(curTag)
                
                self.emissionCounts[(curTag, curWord)] = self.emissionCounts.get((curTag, curWord), 0)+1
                if i == 0:
                    self.initialCounts[curTag] = self.initialCounts.get(curTag, 0)+1
                    self.sentences += 1
                else:
                    lastTag = sentence[i-1][1]
                    self.transitionCounts[(lastTag, curTag)] = self.transitionCounts.get((lastTag, curTag), 0)+1
                

        self.words.add("*")
        vocabSize = len(self.words)
        tagSize = len(self.tags)
        for tag1 in self.tags:
            self.initialProbabilities[tag1] = (1+self.initialCounts.get(tag1, 0))/(tagSize+self.sentences)
            for tag2 in self.tags:
                self.transitionProbabilities[(tag1, tag2)] = (1+self.transitionCounts.get((tag1, tag2), 0))/(self.tagCounts[tag1]+tagSize)
            for word in self.words:
                self.emissionProbabilities[(tag1, word)] = (1+self.emissionCounts.get((tag1, word), 0))/(self.tagCounts[tag1]+vocabSize)

    def viterbi_decode(self, sentence):
        """ Viterbi decoding algorithm implementation

        Arg:
            sentence: a text sequence needed to be decoded
        """
        tokens = sentence.split(" ")
        for i in range(len(tokens)):
            tokens[i] = tokens[i].upper()
        n = len(tokens)
        t = len(self.tags)
        resultTags = [0]*n
        result = [""]*n
        pathProb = [[0]*n for _ in range(t)]   # T rows, N cols
        backPtr = [[None]*n for _ in range(t)]
        idxToTag = {}

        m = 0
        for tag in self.tags:
            idxToTag[m] = tag
            m += 1

        firstWord = tokens[0]
        for i in range(t):
            pathProb[i][0] = self.initialProbabilities[idxToTag[i]]
            if (idxToTag[i], firstWord) in self.emissionProbabilities:
                pathProb[i][0] *= self.emissionProbabilities[(idxToTag[i], firstWord)]
            else:
                pathProb[i][0] *= self.emissionProbabilities[(idxToTag[i], "*")]

        for i in range(1, n):
            for j in range(t):
                bestProb = -1
                bestPath = None
                for k in range(t):
                    prob = pathProb[k][i-1] * self.transitionProbabilities[(idxToTag[k],idxToTag[j])]
                    if (idxToTag[j], tokens[i]) in self.emissionProbabilities:
                        prob *= self.emissionProbabilities[(idxToTag[j], tokens[i])]
                    else:
                        prob *= self.emissionProbabilities[(idxToTag[j], "*")]
                    if prob > bestProb:
                        bestProb = prob
                        bestPath = k
                pathProb[j][i] = bestProb
                backPtr[j][i] = bestPath
                    
        back = pathProb[0][n-1]
        for i in range(t):
            if pathProb[i][n-1] > back:
                back = pathProb[i][n-1]
                resultTags[n-1] = i
        for i in range(n-1, 0, -1):
            resultTags[i-1] = backPtr[resultTags[i]][i]

        for i in range(0, n):
            result[i] = idxToTag[resultTags[i]]
        
        return result
    

if __name__ == "__main__":
    # Initialize the tagger class
    tagger = HMMTagger()

    # Read a corpus and learn from it
    folder_name = input("Input path: ")
    sentences = load_corpus(folder_name)
    tagger.initialize_probabilities(sentences)

    # Test
    sentence = "the planet jupiter and its moons are in effect a mini solar system ."
    result = tagger.viterbi_decode(sentence)
    print(sentence)
    print(result)

    sentence = "computers process programs accurately ."
    result = tagger.viterbi_decode(sentence)
    print(sentence)
    print(result)
