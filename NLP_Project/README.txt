This is the README for Natural Language Processing Project - Trent Haines tsh160230

It will tell you how to run the programs.

please download semantic_relation_classifier.py from this zip file and then open in using Google Colab. Additionally, please place the whole dataset folder containing SemEval2010_task8_all_data within  your Google Drive. 
The path variable is set up so that the program assumes that you will download the corpus as a folder somewhere inside of "My Drive" in your Google Drive.
If you do not do this, please update the gdrive_path variable accordingly. Additionally, if you want to use a different corpus than modified_brown,  or if you do not place the 
corpus directly in "My Drive", then you will need to update the path variables in the bottom of the program where load_corpus is called. Once this is set up, simply run
the whole python file in Colab. Note that the training step may take up to a few minutes, so be patient. The program will print out statistics for the preprocessed data, the training/validation stats,
and the testing stats. It will also print the results for 50 random sentences.