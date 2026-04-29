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


def compute_sentence_score(sentence, LM):
    scores = {};
    if len(sentence) >= 4:
        for i in range(len(sentence) - 3):
            four_gram = tuple(sentence[i:i+4]);
            for lang in LM:
                if lang not in scores:
                    scores[lang] = 0.0;
                if four_gram in LM[lang]:
                    scores[lang] += math.log(LM[lang][four_gram]);
    return scores;


def find_min_threshold(train_file, LM):
    train_file_obj = open(train_file, 'r');
    all_scores = [];
    all_score_diffs = [];
    for line in train_file_obj:
        line = line.strip();
        if not line:
            continue;
        parts = line.split(' ', 1);
        if len(parts) < 2:
            continue;
        label = parts[0];
        text = parts[1];
        scores = compute_sentence_score(text, LM);
        if len(scores) > 0:
            scores_list = list(scores.values());
            score_diff = max(scores_list) - min(scores_list);
            all_score_diffs.append(score_diff);
            if label in scores:
                score = scores[label];
                if score > -200:
                    all_scores.append(score);
    train_file_obj.close();
    if len(all_scores) == 0:
        threshold = -130;
    else:
        all_scores.sort();
        percentile_index = int(len(all_scores) * 0.25);
        threshold = all_scores[percentile_index];
    if len(all_score_diffs) == 0:
        score_diff_threshold = 20;
    else:
        all_score_diffs.sort();
        percentile_index = int(len(all_score_diffs) * 0.05);
        score_diff_threshold = all_score_diffs[percentile_index];
    return threshold, score_diff_threshold;


def test_LM(in_file, out_file, LM, threshold, score_diff_threshold):
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
            if max(scores_list) == min(scores_list) or (best_score < threshold and score_diff < score_diff_threshold):
                likely_language = "other";
        else:
            likely_language = "other";
        out_file.write(likely_language + " " + line + "\n");

# scenario where name of language is in sentence

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
threshold, score_diff_threshold = find_min_threshold(input_file_b, LM)
test_LM(input_file_t, output_file, LM, threshold, score_diff_threshold)
