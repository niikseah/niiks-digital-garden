#!/usr/bin/python3
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import pickle
import struct
import sys
import getopt

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

INT_SIZE = struct.calcsize("I")

def load_dictionary(dict_file):
    with open(dict_file, "rb") as f:
        d = pickle.load(f)
    all_doc_ids = d.get("__doc_ids__", [])
    dictionary = {k: v for k, v in d.items() if k != "__doc_ids__"}
    return dictionary, all_doc_ids

def read_postings_list(postings_file, offset, count):
    """read one postings list: doc_ids then num_skips then (from, to) pairs. returns list of (doc_id, skip_to_or_None)."""
    if count <= 0:
        return []
    with open(postings_file, "rb") as f:
        f.seek(offset)
        doc_ids = list(struct.unpack("I" * count, f.read(count * INT_SIZE)))
        num_skips = struct.unpack("I", f.read(4))[0]
        skip_dict = {}
        for _ in range(num_skips):
            from_idx, to_idx = struct.unpack("II", f.read(2 * INT_SIZE))
            skip_dict[from_idx] = to_idx
    return [(doc_id, skip_dict.get(i)) for i, doc_id in enumerate(doc_ids)]

def intersect_with_skips(list_a, list_b):
    """intersect two postings lists (doc_id, skip_to_or_None), using skip pointers when present. returns list of (doc_id, None)."""
    if not list_a or not list_b:
        return []
    out = []
    i, j = 0, 0
    while i < len(list_a) and j < len(list_b):
        da, skip_a = list_a[i]
        db, skip_b = list_b[j]
        if da == db:
            out.append(da)
            i += 1
            j += 1
        elif da < db:
            if skip_a is not None and list_a[skip_a][0] <= db:
                i = skip_a
            else:
                i += 1
        else:
            if skip_b is not None and list_b[skip_b][0] <= da:
                j = skip_b
            else:
                j += 1
    return [(d, None) for d in out]

def union_lists(list_a, list_b):
    """union two postings lists. returns list of (doc_id, None)."""
    ids_a = [x[0] for x in list_a]
    ids_b = [x[0] for x in list_b]
    return [(d, None) for d in sorted(set(ids_a) | set(ids_b))]

def complement(postings_list, all_doc_ids):
    """doc IDs that are in all_doc_ids but not in postings_list."""
    doc_set = set(p[0] for p in postings_list)
    return sorted(d for d in all_doc_ids if d not in doc_set)

def tokenize_query(line):
    """split query into tokens (terms and operators). handles parentheses and AND, OR, NOT."""
    tokens = []
    for part in line.strip().split():
        part = part.strip()
        if not part:
            continue
        if part in ("AND", "OR", "NOT", "(", ")"):
            tokens.append(part)
        else:
            tokens.append(part)
    return tokens

def shunting_yard(tokens, stemmer):
    """infix Boolean expression to stack form. precedence: () > NOT > AND > OR."""
    precedence = {"OR": 1, "AND": 2, "NOT": 3}
    output = []
    stack = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "(":
            stack.append(t)
            i += 1
        elif t == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if stack:
                stack.pop()
            i += 1
        elif t == "NOT":
            stack.append(t)
            i += 1
        elif t in ("AND", "OR"):
            while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[t]:
                output.append(stack.pop())
            stack.append(t)
            i += 1
        else:
            term = stemmer.stem(t.lower())
            output.append(("term", term))
            i += 1
    while stack:
        op = stack.pop()
        if op != "(" and op != ")":
            output.append(op)
    return output

def evaluate_stack(stack, dictionary, all_doc_ids, postings_file):
    """load postings via seek/read, apply NOT/AND/OR."""
    operand_stack = []
    for x in stack:
        if x == "NOT":
            a = operand_stack.pop()
            if isinstance(a, str):
                a = read_postings_list(postings_file, *dictionary.get(a, (0, 0)))
            operand_stack.append([(d, None) for d in complement(a, all_doc_ids)])
        elif x == "AND":
            b = operand_stack.pop()
            a = operand_stack.pop()
            if isinstance(a, str):
                a = read_postings_list(postings_file, *dictionary.get(a, (0, 0)))
            if isinstance(b, str):
                b = read_postings_list(postings_file, *dictionary.get(b, (0, 0)))
            operand_stack.append(intersect_with_skips(a, b))
        elif x == "OR":
            b = operand_stack.pop()
            a = operand_stack.pop()
            if isinstance(a, str):
                a = read_postings_list(postings_file, *dictionary.get(a, (0, 0)))
            if isinstance(b, str):
                b = read_postings_list(postings_file, *dictionary.get(b, (0, 0)))
            operand_stack.append(union_lists(a, b))
        else:
            _, term = x
            operand_stack.append(term)
    if not operand_stack:
        return []
    top = operand_stack.pop()
    if isinstance(top, str):
        posting = read_postings_list(postings_file, *dictionary.get(top, (0, 0)))
        return [p[0] for p in posting]
    return [p[0] for p in top]

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    if not os.path.isfile(dict_file):
        print("Error: dictionary file not found:", dict_file, file=sys.stderr)
        print("Use actual paths, e.g. -d dictionary.txt -p postings.txt -q sanity-queries.txt -o output.txt", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(postings_file):
        print("Error: postings file not found:", postings_file, file=sys.stderr)
        print("Use actual paths, e.g. -d dictionary.txt -p postings.txt -q sanity-queries.txt -o output.txt", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(queries_file):
        print("Error: queries file not found:", queries_file, file=sys.stderr)
        print("Use actual paths, e.g. -q sanity-queries.txt -o output.txt", file=sys.stderr)
        sys.exit(1)
    dictionary, all_doc_ids = load_dictionary(dict_file)
    stemmer = PorterStemmer()
    results = []
    with open(queries_file, "r", encoding="utf-8", errors="ignore") as qf:
        for line in qf:
            line = line.strip()
            if not line:
                results.append("")
                continue
            tokens = tokenize_query(line)
            if not tokens:
                results.append("")
                continue
            try:
                stack = shunting_yard(tokens, stemmer)
                doc_ids = evaluate_stack(stack, dictionary, all_doc_ids, postings_file)
                results.append(" ".join(map(str, doc_ids)))
            except Exception:
                results.append("")
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
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file is None or postings_file is None or file_of_queries is None or file_of_output is None:
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
