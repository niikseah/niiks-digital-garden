#!/usr/bin/python3
import os
import pickle
import struct
import math
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import sys
import getopt

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print("running search on the queries...")

    if not os.path.isfile(dict_file) or not os.path.isfile(postings_file) or not os.path.isfile(queries_file):
        with open(results_file, "w", encoding="utf-8") as out:
            out.write("")
        return

    with open(dict_file, "rb") as df:
        d = pickle.load(df)

    all_doc_ids = d.get("__doc_ids__", [])
    doc_count = d.get("__doc_count__", len(all_doc_ids))
    doc_lengths = d.get("__doc_lengths__", {})
    dictionary = {
        k: v for k, v in d.items()
        if k not in ("__doc_ids__", "__doc_count__", "__doc_lengths__")
    }
    stemmer = PorterStemmer()

    int_size = struct.calcsize("I")

    def read_postings_list(postings_cursor, offset):
        # random access, use single postings file cursor for random access
        #   seek(offset) -> read df then (docId, tf) tuple for term
        postings_cursor.seek(offset)
        raw_df = postings_cursor.read(int_size)
        if len(raw_df) < int_size:
            return []
        df = struct.unpack("I", raw_df)[0]
        if df <= 0:
            return []
        out = []
        for _ in range(df):
            pair = postings_cursor.read(2 * int_size)
            if len(pair) < 2 * int_size:
                break
            doc_id, tf = struct.unpack("II", pair)
            out.append((doc_id, tf))
        return out

    def tokenize_query(line):
        """
        NLTK sentence + word tokenization (from HW#2: do not line.split())
        """
        tokens = []
        for sent in sent_tokenize(line):
            for token in word_tokenize(sent):
                if not any(c.isalnum() for c in token):
                    continue
                tokens.append(stemmer.stem(token.lower()))
        return tokens

    results = []
    with open(postings_file, "rb") as postings_cursor:
        with open(queries_file, "r", encoding="utf-8", errors="ignore") as qf:
            for line in qf:
                line = line.strip()
                if not line:
                    results.append("")
                    continue
                terms = tokenize_query(line)
                if not terms:
                    results.append("")
                    continue

                # traverse terms in query
                #   if term in dictionary, add 1 to count
                #   if term not in dictionary, create new term with count 1
                #       calculate frequency of term in this query
                query_tf = {}
                for term in terms:
                    query_tf[term] = query_tf.get(term, 0) + 1

                query_weights = {}
                query_sum_sq = 0.0
                for term, tf_q in query_tf.items():
                    # retrieve dF for each term from dictionary
                    #   df = docs that contain t
                    term_meta = dictionary.get(term)
                    if term_meta is None:
                        continue
                    _, df = term_meta
                    if tf_q <= 0 or df <= 0 or doc_count <= 0:
                        continue
                    # calculate idf for the query (ltc):
                    #   idf = log10(N/df), where N = total docs, df = docs containing term
                    idf = math.log(float(doc_count) / float(df), 10)
                    if idf <= 0.0:
                        continue
                    # query weight:
                    #   w = (1 + log10(tf)) * idf
                    w_tq = (1.0 + math.log(float(tf_q), 10)) * idf
                    query_weights[term] = w_tq
                    query_sum_sq += w_tq * w_tq

                if query_sum_sq <= 0.0:
                    results.append("")
                    continue

                # calculate cosine similarity through dot product:
                #   numerator = sum (w / ||q||) * (w / ||d||)
                #   denominator = product of square root of square of normalised query and document
                query_norm = math.sqrt(query_sum_sq)
                scores = {}
                for term, w_tq in query_weights.items():
                    offset, _ = dictionary[term]
                    postings = read_postings_list(postings_cursor, offset)
                    # normalize query vector once:
                    #   w_{t,q}/||q||
                    norm_w_tq = w_tq / query_norm

                    for doc_id, tf_d in postings:
                        if tf_d <= 0:
                            continue
                        doc_norm = doc_lengths.get(doc_id, 0.0)
                        if doc_norm <= 0.0:
                            continue
                        # document weight (lnc, no idf):
                        #   w = 1 + log10(tf)
                        w_td = 1.0 + math.log(float(tf_d), 10)
                        # cosine contribution for this term:
                        #   (w / ||q||) * (w / ||d||)
                        contribution = norm_w_tq * (w_td / doc_norm)
                        scores[doc_id] = scores.get(doc_id, 0.0) + contribution

                # return top 10 documents
                #   if less than 10 documents, return all
                #   rank by score desc
                #   if same score, rank by docId asc
                # return top 10 documents:
                #   rank by score desc, then docID asc for ties
                ranked = sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:10]
                results.append(" ".join(str(doc_id) for doc_id, _ in ranked))

    with open(results_file, "w", encoding="utf-8") as out:
        out.write("\n".join(results) + ("\n" if results else ""))

dictionary_file = postings_file = file_of_queries = file_of_output = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
