This is the README for Natural Language Processing Homework 2 - Trent Haines tsh160230

It will tell you how to run the programs.

Part 1:
	In order to run part 1, please download Viterbi.py from this same zip file and then run the following command in terminal: python3 hw2part1.py
	The program will then ask the user to input a path to the corpus directory. The program handles the path up to the directory of the program, so please
	enter a relative path for the corpus path. For example, if we download the python program and the modified_brown corpus in the same directory, we would simply
	enter "modified_brown" in to the terminal when it asks us for the path. The program should then run the functions and print the two provided example sentences
	and results, a list of tags, for those sentences. 
	
Part 2:
	In order to run part 2, please download KerasLSTMRNN.py from this zip file and then open in using Google Colab. Additionally, please place the modified_brown corpus you are training
	in your Google Drive. The path variable is set up so that the program assumes that you will download the corpus as a folder somewhere inside of "My Drive" in your Google Drive.
	If you do not do this, please update the gdrive_path variable accordingly. Additionally, if you want to use a different corpus than modified_brown,  or if you do not place the 
	corpus directly in "My Drive", then you will need to update the path variable right below the load_corpus function, as this is the path that specifies the location of the corpus 
	relative to "My Drive". No variables will need to be changed if you have modified_brown corpus folder directly in "My Drive" in your Google Drive. Once this is set up, simply run
	the whole python file in Colab. Note that the training step may take up to a few minutes, so be patient. The program will print out the two example sentences as well as their
	corresponding output, being a list of tags.