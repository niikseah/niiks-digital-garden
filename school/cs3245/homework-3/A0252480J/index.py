#!/usr/bin/python3
import os
import struct
import pickle
import math
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import sys
import getopt

# index.py
# tokenize, stem, case fold
# traverse terms in document
    # if term in dictionary, add 1 to count
    # if term not in dictionary, create new term with count 1
        # calculate frequency of term, and create a tuple (docId, frequency)
    # calculate dF for each term 
    # calculate normalised document length here to make search run faster

# for each term, calculate tf for document
    # (1 + log(tf)) 
        # tf 0, weighted tf 0 

# search.py
# tokenize, stem, case fold
# traverse terms in query
    # if term in dictionary, add 1 to count
    # if term not in dictionary, create new term with count 1
        # calculate frequency of term, and create a tuple (docId, frequency)

# for each term, calculate tf-idf for query
    # retrieve dF for each term
    # (1 + log(tf)) * log(N/df), where N is number of documents 
        # if math.log(0, 10) return 0

# calculate cosine similarity through dot product of query and document for each query (dot product / product of square root of square of cos similarity of query and document)
    # retrieve normalised document length from dictionary
        # rank cosine similarity

# return top 10 documents
    # if less than 10 documents, return all
# rank by score
    # if same score, rank by docId

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print("indexing...")

    stemmer = PorterStemmer()
    # term -> {doc_id: tf} in postings list
    inverted_index = {}
    # doc_id -> vector norm for lnc document weighting
    doc_lengths = {}
    doc_ids = []

    # for each document d:
    #   tokenize + stem + case-fold
    #   traverse terms in document
    #   compute tf
    #   compute document weight per term:
    #       w = 1 + log10(tf)
    #   compute doc normalisation:
    #       docLength = sqrt( sum (w^2) )
    #   store postings (docId, tf) + df per term

    try:
        filenames = sorted(os.listdir(in_dir), key=lambda f: int(f) if f.isdigit() else 0)
    except (ValueError, TypeError):
        filenames = sorted(os.listdir(in_dir))

    for name in filenames:
        path = os.path.join(in_dir, name)
        if not (os.path.isfile(path) and name.isdigit()):
            continue
        doc_id = int(name)
        doc_ids.append(doc_id)

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                text = fp.read()
        except OSError:
            continue

        # traverse terms in document
        #   if term in dictionary, add 1 to count
        #   if term not in dictionary, create new term with count 1
        #       calculate frequency of term, create (term -> tf)
        term_counts = {}
        for sent in sent_tokenize(text):
            for token in word_tokenize(sent):
                if not any(c.isalnum() for c in token):
                    continue
                term = stemmer.stem(token.lower())
                term_counts[term] = term_counts.get(term, 0) + 1

        # calculate docLength
        #   for each term, calculate tf for document
        #       (1 + log(tf)) 
        sum_sq = 0.0
        for term, tf in term_counts.items():
            weight = 1.0 + math.log(tf, 10)
            sum_sq += weight * weight
            if term not in inverted_index:
                inverted_index[term] = {}
            inverted_index[term][doc_id] = tf
        doc_lengths[doc_id] = math.sqrt(sum_sq) if sum_sq > 0.0 else 0.0

    dictionary = {}
    with open(out_postings, "wb") as pf:
        for term in sorted(inverted_index.keys()):
            # calculate dF for each term
            postings_items = sorted(inverted_index[term].items(), key=lambda x: x[0])
            df = len(postings_items)
            offset = pf.tell()
            # postings on disk:
            #   [df] then df pairs of (doc_id, tf)
            pf.write(struct.pack("I", df))
            for doc_id, tf in postings_items:
                # posting tuple is (doc_id, tf)
                pf.write(struct.pack("I", doc_id))
                pf.write(struct.pack("I", tf))
            dictionary[term] = (offset, df)

    dictionary["__doc_ids__"] = sorted(doc_ids)
    dictionary["__doc_count__"] = len(doc_ids)
    dictionary["__doc_lengths__"] = doc_lengths
    with open(out_dict, "wb") as df:
        pickle.dump(dictionary, df)

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
