#!/bin/bash

if [ $# -ne 2 ]; then
   echo "RUN BY TYPING INTO TERMIMAL: ./ngrams.sh corpusFileName smoothing"
   exit 1
fi

python3 hw1.py $1 $2