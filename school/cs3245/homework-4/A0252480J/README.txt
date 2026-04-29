This is the README file for A0252480J's submission
Email: e0958068@u.nus.edu 

== Python Version ==

I'm using Python Version 3.14.2 for this assignment.

== General Notes about this assignment ==

index: reads legal cases from a csv corpus with fields
'document_id,title,content,date_posted,court'

each document is tokenized by regex and casefolded, then stemmed using Porter stemmer.

weighted term frequencies are computed per zone:
content=2, title=5, court=3, date_posted=1

for each term, postings are stored on disk as '(doc_id, weighted_tf)' pairs.

dictionary stores term -> (offset, df), and document lengths are precomputed for faster search.



search: reads one query from the first non-empty line of the query file.

query is cleaned of quotes and AND operators, then tokenized/casefolded/stemmed.

lnc.ltc cosine similarity ranking is used.

manual-thesaurus query expansion is implemented with a lower expansion weight (EXPANSION_ALPHA = 0.35),
with value selection guided by common PRF interpolation / expansion-weight defaults in Anserini.

ranking order is produced using a heap-based step, then output as space-separated document ids in one line.

== Files included with this submission ==

`index.py` - builds dictionary and postings files from the legal csv corpus.
`search.py` - runs ranked retrieval using lnc.ltc cosine similarity with query expansion.
`dictionary.txt` - pickled dictionary mapping terms to '(offset, df)' plus metadata.
`postings.txt` - binary postings lists stored as '[df][(doc_id, weighted_tf)...]'.
`README.txt` - documentation.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0252480J, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Gilligan's Island Rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

== References ==

school/cs3245/homework-3 code and structure for tf-idf/cosine retrieval adaptation
- NLTK documentation (Porter stemmer): https://www.nltk.org/
- Python docs: pickle (https://docs.python.org/3/library/pickle.html), struct (https://docs.python.org/3/library/struct.html), heapq (https://docs.python.org/3/library/heapq.html)
- CS3245 lecture notes for lnc.ltc weighting and vector-space retrieval
- Anserini query reranking docs (RM3/BM25PRF weighting defaults): https://mintlify.wiki/castorini/anserini/search/reranking