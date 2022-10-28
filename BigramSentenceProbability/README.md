Natural Language Processing Homework 1
Author: Trent Haines
NetID: tsh160230

This project has a Bigram language model trained on a specified corpus in order to generate the bigram count tables, bigram probabilities tables, and total sentence probabilities for two predefined sentences.
The program supports the ability to test with add-one smoothing and without add-one smoothing. 
To run the program, please put all of the uploaded files in a single directory with python3 installed.
After the program outputs the required tables and probabilities, the program asks the user through terminal input for any bigram probability queries.
The user can then type a query in the format 'word1 word2', where the space separated words represent asking for the probability of word2 given word1.
The program will then print out the corresponding probability. If the input is not given in this format, the probability will be printed out as 0.
The user can ask as many queries as they want, and it will run on the smoothing model specified at command execution. To stop the program, use Ctrl+C.

Once all of the files are in a directory, type the following into terminal: ./ngrams.sh training-set b
'training-set' represents a text file that has the relative path of the corpus e.g corpus.txt
'b' represents a number in the set {0, 1}, 0 meaning that the program will not use add-one smoothing, and 1 meaning that the program will utilize add-one smoothing

The program assumes that punctuation does not belong to tokens, and only alphanumeric words separated by whitespace and or punctuation count as tokens, as per recommendation.
The program factors in a sentence start symbol into the total bigram probability calculations, as seen in the examples in class. 