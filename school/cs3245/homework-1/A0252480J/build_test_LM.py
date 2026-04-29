#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
import sys
import getopt
import math

"""
ideation: 

build:
1. take first word of each line to determine language
2. use nltk to tokenize the remaining tokens in the sentence
3. take every 4 tokens to create a 4-gram (overlap!)
4. count the frequency of each 4-gram
5. apply one-smoothing
6. calculate the probability of each 4-gram
7. store probabilities in a dictionary

test:
1. tokenize test string
2. combine probabilities to get a score
3. highest score highest probability

"""

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")
    # This is an empty method
    # Pls implement your code below

    # open file for reading
    in_file = open(in_file, 'r')

    # initialise LanguageModel
    LM = {};

    # initialise MasterList
    ML = {};

    # initialise ProbabilityList
    PL = {};

    # first word to determine language
    for line in in_file:
        line = line.strip();
        if not line:
            continue;
        # if first time appearing, create dictionary
        # split by any whitespace but grab the first item (which is the first word)
        first_word = line.split()[0];
        if first_word not in LM:
            LM[first_word] = {};
    # tokenize remaining sentence
        # grabs everything after the first word, [1] takes second part of the split where line.split(' ',1) splits it at first space only
        remaining_sentence = line.split(' ', 1)[1];
        # last 3 letters cannot create 4-gram
        for i in range(len(remaining_sentence) - 3):
        # create 4-grams
            # tuples because lists cannot be keys
            four_gram = tuple(remaining_sentence[i:i+4]);
            # initialise dictionary entry, save to dictionary, count frequency
            if four_gram not in LM[first_word]:
                LM[first_word][four_gram] = 0;
            if four_gram not in ML:
                ML[four_gram] = 1;
            LM[first_word][four_gram] += 1;

    # count the frequency of each 4-gram
    # add one-smoothing
    for first_word in LM:
        for four_gram in ML:
            if four_gram not in LM[first_word]:
                LM[first_word][four_gram] = 1;
            else:
                LM[first_word][four_gram] += 1;

    # calculate probability 
    for first_word in LM:
        PL[first_word] = {};
        for four_gram in LM[first_word]:
            PL[first_word][four_gram] = LM[first_word][four_gram] / sum(LM[first_word].values());
    #store probability in dictionary
    return PL;


def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    # This is an empty method
    # Pls implement your code below

    # open files for reading and writing
    in_file = open(in_file, 'r')
    out_file = open(out_file, 'w')

    # initialise ScoreList
    SL = {};

    for line in in_file:
        line = line.strip();
        if not line:
            continue;
        # initialise TestDictionary for this line
        TD = {};
        # tokenize test string
        for i in range(len(line) - 3):
            test_four_gram = tuple(line[i:i+4]);
            if test_four_gram not in TD:
                TD[test_four_gram] = 1;
        # combine probabilities to get a score
        for first_word in LM:
            SL[first_word] = 0.0; 
            for test_four_gram in TD:
                # watch out for this case first in case of key error
                if test_four_gram in LM[first_word]:
                    SL[first_word] += math.log(LM[first_word][test_four_gram]);
        # highest score highest probability
        # max of keys, key is placed in lambda to return SL[l]
        if len(SL) > 0:
            likely_language = max(SL.keys(), key=lambda l: SL[l]);
            best_score = SL[likely_language];
            
            scores_list = list(SL.values());
            score_diff = max(scores_list) - min(scores_list);
            # if same or zero == alien 
            if max(scores_list) == min(scores_list):
                likely_language = "other";
        else:
            likely_language = "other";

        out_file.write(likely_language + " " + line + "\n");


def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"

if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)

test_LM(input_file_t, output_file, LM)
