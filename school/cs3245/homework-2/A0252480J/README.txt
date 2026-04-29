This is the README file for A0252480J's submission
Email: e0958068@u.nus.edu 

== Python Version ==

I'm using Python Version 3.14.2 for
this assignment.

== General Notes about this assignment ==

Documents tokenized by sentences first using NLTK sent_tokenize, then by words using word_tokenize.
Tokens stemmed with Porter stemmer and case-folded.
SPIMI used: 
1. documents processed in blocks (block size 2500 to ensure >=2 blocks to be merged)
2. block written to temporary file
3. blocks merged into single postings file
4. math.sqrt(length) skip pointers evenly placed
5. dictionary maps each term to (offset, count) and stored with pickle [for NOT, doc_ids saved]

To search, dictionary is loaded from disk.
For each query line, tokens parsed and Boolean expressions are converted to stack form
Stack evaluated: postings lists loaded via seek/read
single terms use dictionary pointer
AND uses intersection
OR uses union
NOT uses complement of doc IDs saved
results returned in their own line

== Files included with this submission ==

README.txt - documentation of work done
index.py - to index documents: SPIMI, block merge, skip pointers, dictionary write, postings write
search.py - to search: Boolean query parser
dictionary.txt - saved dictionary (term -> (offset, count)) and doc IDs
postings.txt - binary postings file (doc IDs per term, then skip pointer pairs).

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0252480J, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Gilligan's Island Rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==

- CS3245 Lecture 2 and 3 slides
- NLTK documentation (tokenization, Porter stemmer): https://www.nltk.org/
- Shunting-yard algorithm: https://en.wikipedia.org/wiki/Shunting-yard_algorithm
- Python docs: pickle (https://docs.python.org/3/library/pickle.html), struct (https://docs.python.org/3/library/struct.html).
