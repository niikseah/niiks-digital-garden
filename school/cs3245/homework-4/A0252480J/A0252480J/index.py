#!/usr/bin/python3
import csv
import getopt
import math
import pickle
import re
import struct
import sys
from collections import defaultdict

from nltk.stem.porter import PorterStemmer


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")

# Lightweight stopword list to reduce noisy index entries.
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "but", "by",
    "for", "from", "had", "has", "have", "he", "her", "hers", "him", "his",
    "i", "if", "in", "into", "is", "it", "its", "itself", "me", "my", "of",
    "on", "or", "our", "ours", "she", "so", "that", "the", "their", "them",
    "they", "this", "to", "too", "was", "we", "were", "what", "when", "which",
    "who", "whom", "why", "will", "with", "you", "your", "yours",
}

# Zone-aware term-frequency weighting.
CONTENT_WEIGHT = 2
TITLE_WEIGHT = 5
COURT_WEIGHT = 3
DATE_WEIGHT = 1


def usage():
    print("usage: " + sys.argv[0] + " -i dataset-file -d dictionary-file -p postings-file")


def tokenize(text, stemmer):
    out = []
    for raw in TOKEN_PATTERN.findall(text or ""):
        lowered = raw.lower()
        if lowered.isalpha() and lowered in STOPWORDS:
            continue
        if lowered.isalpha() and len(lowered) == 1:
            continue
        out.append(stemmer.stem(lowered))
    return out


def add_weighted_tokens(term_counts, text, weight, stemmer):
    if weight <= 0:
        return
    for term in tokenize(text, stemmer):
        term_counts[term] += weight


def parse_doc_id(row):
    raw_doc_id = row.get("document_id")
    if raw_doc_id is None:
        return None
    try:
        return int(raw_doc_id)
    except ValueError:
        return None


def build_doc_term_counts(row, stemmer):
    term_counts = defaultdict(int)
    add_weighted_tokens(term_counts, row.get("content", ""), CONTENT_WEIGHT, stemmer)
    add_weighted_tokens(term_counts, row.get("title", ""), TITLE_WEIGHT, stemmer)
    add_weighted_tokens(term_counts, row.get("court", ""), COURT_WEIGHT, stemmer)
    add_weighted_tokens(term_counts, row.get("date_posted", ""), DATE_WEIGHT, stemmer)
    return term_counts


def compute_doc_length_and_update_index(doc_id, term_counts, inverted_index):
    if not term_counts:
        return 0.0

    sum_sq = 0.0
    for term, tf in term_counts.items():
        weight = 1.0 + math.log(float(tf), 10)
        sum_sq += weight * weight
        inverted_index[term][doc_id] = tf
    return math.sqrt(sum_sq) if sum_sq > 0.0 else 0.0


def iterate_corpus_rows(in_dataset):
    with open(in_dataset, "r", encoding="utf-8", errors="ignore", newline="") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            yield row


def build_in_memory_index(in_dataset, stemmer):
    inverted_index = defaultdict(dict)
    doc_lengths = {}
    doc_ids = []

    for row in iterate_corpus_rows(in_dataset):
        doc_id = parse_doc_id(row)
        if doc_id is None:
            continue
        term_counts = build_doc_term_counts(row, stemmer)
        doc_lengths[doc_id] = compute_doc_length_and_update_index(doc_id, term_counts, inverted_index)
        doc_ids.append(doc_id)

    return inverted_index, doc_lengths, doc_ids


def write_postings_and_dictionary(out_postings, inverted_index):
    dictionary = {}
    with open(out_postings, "wb") as pf:
        for term in sorted(inverted_index.keys()):
            postings_items = sorted(inverted_index[term].items(), key=lambda pair: pair[0])
            offset = pf.tell()
            df = len(postings_items)
            pf.write(struct.pack("I", df))
            for doc_id, tf in postings_items:
                pf.write(struct.pack("II", doc_id, tf))
            dictionary[term] = (offset, df)
    return dictionary


def write_dictionary_file(out_dict, dictionary):
    with open(out_dict, "wb") as df:
        pickle.dump(dictionary, df, protocol=pickle.HIGHEST_PROTOCOL)


def build_index(in_dataset, out_dict, out_postings):
    print("indexing...")
    stemmer = PorterStemmer()
    csv.field_size_limit(sys.maxsize)
    try:
        inverted_index, doc_lengths, doc_ids = build_in_memory_index(in_dataset, stemmer)
    except OSError as exc:
        print(f"failed to read dataset: {exc}", file=sys.stderr)
        raise

    dictionary = write_postings_and_dictionary(out_postings, inverted_index)

    dictionary["__doc_ids__"] = sorted(doc_ids)
    dictionary["__doc_count__"] = len(doc_ids)
    dictionary["__doc_lengths__"] = doc_lengths
    write_dictionary_file(out_dict, dictionary)


input_dataset = output_file_dictionary = output_file_postings = None

try:
    opts, _ = getopt.getopt(sys.argv[1:], "i:d:p:")
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt == "-i":
        input_dataset = arg
    elif opt == "-d":
        output_file_dictionary = arg
    elif opt == "-p":
        output_file_postings = arg
    else:
        assert False, "unhandled option"

if input_dataset is None or output_file_dictionary is None or output_file_postings is None:
    usage()
    sys.exit(2)

build_index(input_dataset, output_file_dictionary, output_file_postings)
