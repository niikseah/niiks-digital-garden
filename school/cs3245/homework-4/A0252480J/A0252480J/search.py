#!/usr/bin/python3
import getopt
import heapq
import math
import os
import pickle
import re
import struct
import sys
from collections import defaultdict

from nltk.stem.porter import PorterStemmer


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?")
PHRASE_PATTERN = re.compile(r'"([^"]+)"')

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "but", "by",
    "for", "from", "had", "has", "have", "he", "her", "hers", "him", "his",
    "i", "if", "in", "into", "is", "it", "its", "itself", "me", "my", "of",
    "on", "or", "our", "ours", "she", "so", "that", "the", "their", "them",
    "they", "this", "to", "too", "was", "we", "were", "what", "when", "which",
    "who", "whom", "why", "will", "with", "you", "your", "yours",
}

# Query refinement (manual thesaurus expansion).
LEGAL_QUERY_EXPANSIONS_RAW = {
    "damages": ["compensation", "injury", "loss", "negligence"],
    "phone": ["telephone", "call", "communication"],
    "quiet": ["silent", "silence"],
    "fertility": ["pregnancy", "medical", "treatment"],
    "grades": ["marks", "results", "academic"],
    "exchange": ["swap", "trade", "transfer"],
    "scandal": ["fraud", "misconduct", "corruption"],
    "murder": ["homicide", "kill", "manslaughter"],
    "contract": ["agreement", "breach", "consideration"],
    "appeal": ["appellant", "respondent", "judgment"],
}

EXPANSION_ALPHA = 0.35


def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -d dictionary-file -p postings-file -q query-file -o output-file-of-results"
    )


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


def build_expansion_map(stemmer):
    expanded = {}
    for key, values in LEGAL_QUERY_EXPANSIONS_RAW.items():
        stemmed_key = stemmer.stem(key.lower())
        bucket = set(expanded.get(stemmed_key, []))
        for term in values:
            stemmed_term = stemmer.stem(term.lower())
            if stemmed_term != stemmed_key:
                bucket.add(stemmed_term)
        expanded[stemmed_key] = sorted(bucket)
    return expanded


def parse_query_line(query_line, stemmer):
    query_no_phrases = PHRASE_PATTERN.sub(" ", query_line)
    query_no_ops = re.sub(r"\bAND\b", " ", query_no_phrases, flags=re.IGNORECASE)
    return tokenize(query_no_ops, stemmer)


def read_first_query_line(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fp:
            for line in fp:
                text = line.strip()
                if text:
                    return text
    except OSError:
        return ""
    return ""


def write_empty_result(results_file):
    with open(results_file, "w", encoding="utf-8") as out:
        out.write("\n")


def load_dictionary_payload(dict_file):
    with open(dict_file, "rb") as df:
        return pickle.load(df)


def unpack_dictionary(payload):
    doc_count = payload.get("__doc_count__", 0)
    doc_lengths = payload.get("__doc_lengths__", {})
    dictionary = {
        k: v
        for k, v in payload.items()
        if k not in ("__doc_ids__", "__doc_count__", "__doc_lengths__")
    }
    return dictionary, doc_count, doc_lengths


def build_base_term_frequencies(base_terms):
    base_tf = defaultdict(int)
    for term in base_terms:
        base_tf[term] += 1
    return base_tf


def build_raw_query_weights(base_tf, expansion_map):
    raw_query_weights = defaultdict(float)
    for term, tf in base_tf.items():
        raw_query_weights[term] += 1.0 + math.log(float(tf), 10)

    for term, tf in base_tf.items():
        source_weight = 1.0 + math.log(float(tf), 10)
        for expanded_term in expansion_map.get(term, []):
            raw_query_weights[expanded_term] += EXPANSION_ALPHA * source_weight

    return raw_query_weights


def build_query_weights(raw_query_weights, dictionary, doc_count):
    query_weights = {}
    query_sq_sum = 0.0

    for term, raw_weight in raw_query_weights.items():
        if raw_weight <= 0.0:
            continue
        meta = dictionary.get(term)
        if meta is None:
            continue
        _, df = meta
        if df <= 0:
            continue
        idf = math.log(float(doc_count) / float(df), 10)
        if idf <= 0.0:
            continue
        w_tq = raw_weight * idf
        query_weights[term] = w_tq
        query_sq_sum += w_tq * w_tq

    query_norm = math.sqrt(query_sq_sum) if query_sq_sum > 0.0 else 0.0
    return query_weights, query_norm


def read_postings_list(postings_fp, offset, int_size):
    postings_fp.seek(offset)
    raw_df = postings_fp.read(int_size)
    if len(raw_df) < int_size:
        return []
    df = struct.unpack("I", raw_df)[0]
    postings = []
    for _ in range(df):
        pair = postings_fp.read(2 * int_size)
        if len(pair) < 2 * int_size:
            break
        postings.append(struct.unpack("II", pair))
    return postings


def get_cached_postings(term, dictionary, postings_fp, int_size, cache):
    if term in cache:
        return cache[term]
    meta = dictionary.get(term)
    if meta is None:
        cache[term] = []
        return cache[term]
    offset, _ = meta
    cache[term] = read_postings_list(postings_fp, offset, int_size)
    return cache[term]


def score_documents(query_weights, query_norm, dictionary, postings_file, doc_lengths):
    if query_norm <= 0.0:
        return {}

    with open(postings_file, "rb") as pf:
        postings_cache = {}
        int_size = struct.calcsize("I")
        scores = defaultdict(float)

        for term, w_tq in query_weights.items():
            norm_w_tq = w_tq / query_norm
            postings = get_cached_postings(term, dictionary, pf, int_size, postings_cache)
            for doc_id, tf_d in postings:
                doc_norm = doc_lengths.get(doc_id, 0.0)
                if tf_d <= 0 or doc_norm <= 0.0:
                    continue
                w_td = 1.0 + math.log(float(tf_d), 10)
                scores[doc_id] += norm_w_tq * (w_td / doc_norm)
    return scores


def rank_documents_with_heap(scores):
    heap = [(-score, doc_id) for doc_id, score in scores.items()]
    heapq.heapify(heap)
    ranked = []
    while heap:
        neg_score, doc_id = heapq.heappop(heap)
        ranked.append((doc_id, -neg_score))
    return ranked


def run_search(dict_file, postings_file, query_file, results_file):
    print("running search on the query...")
    if (
        not os.path.isfile(dict_file)
        or not os.path.isfile(postings_file)
        or not os.path.isfile(query_file)
    ):
        write_empty_result(results_file)
        return

    payload = load_dictionary_payload(dict_file)
    dictionary, doc_count, doc_lengths = unpack_dictionary(payload)
    if doc_count <= 0:
        write_empty_result(results_file)
        return

    stemmer = PorterStemmer()
    query_line = read_first_query_line(query_file)
    if not query_line:
        write_empty_result(results_file)
        return

    base_terms = parse_query_line(query_line, stemmer)
    if not base_terms:
        write_empty_result(results_file)
        return

    expansion_map = build_expansion_map(stemmer)
    base_tf = build_base_term_frequencies(base_terms)
    raw_query_weights = build_raw_query_weights(base_tf, expansion_map)
    query_weights, query_norm = build_query_weights(raw_query_weights, dictionary, doc_count)
    if query_norm <= 0.0:
        write_empty_result(results_file)
        return

    scores = score_documents(query_weights, query_norm, dictionary, postings_file, doc_lengths)
    ranked = rank_documents_with_heap(scores)
    output_line = " ".join(str(doc_id) for doc_id, _ in ranked)

    with open(results_file, "w", encoding="utf-8") as out:
        out.write(output_line + "\n")


dictionary_file = postings_file = query_file = output_file = None

try:
    opts, _ = getopt.getopt(sys.argv[1:], "d:p:q:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt == "-d":
        dictionary_file = arg
    elif opt == "-p":
        postings_file = arg
    elif opt == "-q":
        query_file = arg
    elif opt == "-o":
        output_file = arg
    else:
        assert False, "unhandled option"

if dictionary_file is None or postings_file is None or query_file is None or output_file is None:
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, query_file, output_file)
