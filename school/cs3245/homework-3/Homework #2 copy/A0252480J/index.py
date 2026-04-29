#!/usr/bin/python3
import math
import os
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import sys
import getopt
import struct
import pickle
import tempfile

# reuters 7k docs, SPIMI block size for 2+ blocks 
BLOCK_DOCS = 2500

INT_SIZE = struct.calcsize("I")
SHORT_SIZE = struct.calcsize("H")

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def normalise_dir(path):
    """ensure directory path has only 1 trailing slash (Windows)."""
    path = path.rstrip(os.sep)
    return path + os.sep

def tokenize_and_stem(text):
    """
    tokenize by sentence, then by word; stem with Porter; case-fold.
    returns list of normalised terms.
    """
    stemmer = PorterStemmer()
    terms = []
    for sent in sent_tokenize(text):
        for word in word_tokenize(sent):
            terms.append(stemmer.stem(word.lower()))
    return terms

def write_block(block_index, block_path, index):
    """write one SPIMI block to disk: num_entries then (term_len, term, doc_count, doc_ids) per term."""
    sorted_terms = sorted(index.keys())
    with open(block_path, "wb") as f:
        f.write(struct.pack("I", len(sorted_terms)))
        for term in sorted_terms:
            doc_list = sorted(set(index[term]))
            term_bytes = term.encode("utf-8")
            f.write(struct.pack("H", len(term_bytes)))
            f.write(term_bytes)
            f.write(struct.pack("I", len(doc_list)))
            for d in doc_list:
                f.write(struct.pack("I", d))

def read_block_entry(f):
    """
    read one (term, doc_list) from an open block file (after num_entries was read). 
    returns (term, doc_list) or (None, None) at EOF.
    """
    term_len_bytes = f.read(2)
    # 2 means 2 bytes to store term length
    if len(term_len_bytes) < 2:
        return (None, None)
    term_len = struct.unpack("H", term_len_bytes)[0]
    # returns tuple, [0] extracts first elem
    term = f.read(term_len).decode("utf-8")
    doc_count = struct.unpack("I", f.read(4))[0]
    doc_list = list(struct.unpack("I" * doc_count, f.read(doc_count * INT_SIZE)))
    return (term, doc_list)

def merge_blocks(block_paths, out_postings):
    """merge SPIMI blocks into one postings file (term order). returns dict term -> (offset, count)."""
    files = [open(p, "rb") for p in block_paths]
    num_entries_list = [struct.unpack("I", f.read(4))[0] for f in files]
    current = []  # (term, doc_list, block_id)
    for i, f in enumerate(files):
        if num_entries_list[i] > 0:
            t, lst = read_block_entry(f)
            if t is not None:
                current.append((t, lst, i))
                num_entries_list[i] -= 1

    dictionary = {}
    current_offset = 0
    with open(out_postings, "wb") as out:
        while current:
            current.sort(key=lambda x: x[0])
            term = current[0][0]
            merged = []
            consumed_blocks = []
            i = 0
            while i < len(current) and current[i][0] == term:
                _, lst, bid = current[i]
                merged.extend(lst)
                consumed_blocks.append(bid)
                i += 1
            merged = sorted(set(merged))
            out.write(struct.pack("I", len(merged)))
            for d in merged:
                out.write(struct.pack("I", d))
            dictionary[term] = (current_offset, len(merged))
            current_offset += INT_SIZE + len(merged) * INT_SIZE
            current = current[i:]
            for bid in consumed_blocks:
                if num_entries_list[bid] > 0:
                    t, lst = read_block_entry(files[bid])
                    if t is not None:
                        current.append((t, lst, bid))
                        num_entries_list[bid] -= 1
    for f in files:
        f.close()
    return dictionary

def add_skip_pointers(postings_path, dict_term_to_offset_count, out_postings):
    """
    read postings list by list, add sqrt(n) evenly placed skip pointers, write updated index.
    on disk: doc_ids (count * 4 bytes), then num_skips (4), then only (from_index, to_index) for each skip.
    """
    tmp_path = out_postings + ".tmp"
    sorted_terms = sorted(dict_term_to_offset_count.keys())
    new_dictionary = {}
    current_offset = 0
    with open(postings_path, "rb") as fin:
        with open(tmp_path, "wb") as fout:
            for term in sorted_terms:
                offset, count = dict_term_to_offset_count[term]
                fin.seek(offset)
                count_val = struct.unpack("I", fin.read(4))[0]
                doc_ids = list(struct.unpack("I" * count_val, fin.read(count_val * INT_SIZE)))
                n = len(doc_ids)
                skip_count = max(0, int(math.sqrt(n)))
                if skip_count > 0:
                    step = n // skip_count
                else:
                    step = n + 1
                skip_pairs = []
                for i in range(skip_count):
                    pos = i * step
                    next_pos = (i + 1) * step
                    if next_pos < n:
                        skip_pairs.append((pos, next_pos))
                for doc_id in doc_ids:
                    fout.write(struct.pack("I", doc_id))
                fout.write(struct.pack("I", len(skip_pairs)))
                for from_idx, to_idx in skip_pairs:
                    fout.write(struct.pack("I", from_idx))
                    fout.write(struct.pack("I", to_idx))
                new_dictionary[term] = (current_offset, n)
                current_offset += n * INT_SIZE + 4 + len(skip_pairs) * 2 * INT_SIZE
    os.replace(tmp_path, out_postings)
    return new_dictionary

def build_index(in_dir, out_dict, out_postings):
    """
    build index with SPIMI, then merge blocks, then add skip pointers and write final index.
    """
    in_dir = normalise_dir(in_dir)
    if not os.path.isdir(in_dir) and "nltk_data" in in_dir:
        rest = in_dir.split("nltk_data", 1)[-1].lstrip(os.sep).rstrip(os.sep)
        if rest:
            for data_dir in nltk.data.path:
                attempt = normalise_dir(os.path.join(data_dir, rest))
                if os.path.isdir(attempt):
                    in_dir = attempt
                    break
    print("indexing...")

    try:
        filenames = sorted(os.listdir(in_dir), key=lambda f: int(f) if f.isdigit() else 0)
    except (ValueError, TypeError):
        filenames = sorted(os.listdir(in_dir))

    doc_ids = []
    for f in filenames:
        if os.path.isfile(os.path.join(in_dir, f)) and f.isdigit():
            doc_ids.append(int(f))

    # SPIMI
    block_paths = []
    index = {}
    docs_in_block = 0
    for doc_id in doc_ids:
        path = os.path.join(in_dir, str(doc_id))
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                text = fp.read()
        except OSError:
            continue
        terms = tokenize_and_stem(text)
        for term in set(terms):
            if term not in index:
                index[term] = []
            index[term].append(doc_id)
        docs_in_block += 1
        if docs_in_block >= BLOCK_DOCS:
            fd, block_path = tempfile.mkstemp(suffix=".block", prefix="spimi_")
            os.close(fd)
            write_block(len(block_paths), block_path, index)
            block_paths.append(block_path)
            index = {}
            docs_in_block = 0

    if index:
        fd, block_path = tempfile.mkstemp(suffix=".block", prefix="spimi_")
        os.close(fd)
        write_block(len(block_paths), block_path, index)
        block_paths.append(block_path)

    if not block_paths:
        # no documents
        with open(out_dict, "wb") as df:
            pickle.dump({}, df)
        with open(out_postings, "wb") as pf:
            pass
        print("done.")
        return

    # merge blocks into one postings file (no skip pointers yet)
    temp_postings = out_postings + ".no_skip"
    dictionary = merge_blocks(block_paths, temp_postings)
    for p in block_paths:
        try:
            os.remove(p)
        except OSError:
            pass

    # add skip pointers and write final dictionary and postings
    new_dict = add_skip_pointers(temp_postings, dictionary, out_postings)
    try:
        os.remove(temp_postings)
    except OSError:
        pass
    # store all doc IDs for NOT queries
    new_dict["__doc_ids__"] = sorted(doc_ids)
    with open(out_dict, "wb") as df:
        pickle.dump(new_dict, df)

    print("done.")

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
