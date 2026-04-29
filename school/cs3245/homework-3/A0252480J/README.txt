This is the README file for A0252480J's submission
Email: e0958068@u.nus.edu (If you do not have an email address in this format, please use your standard NUS Email.)

== Python Version ==

I'm (We're) using Python Version 3.14.2 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

index: each doc is tokenized and casefolded using NLTK, stemmed using Porter. 
term frequency per document is computed, with postings stored on disk as '(doc_id, tf)' pairs for each term.
for each term, dictionary stores file offset where postings list begins, and document frequency.
document length is precomputed for search.py to run faster, to be used in lnc weighting scheme.

search: lnc.ltc cosine similarity model with ranked retrieval used as assigned.
every query line is tokenized and casefolded using NLTK, stemmed using Porter.
term frequencies computed
to avoid keeping postings in memory, one file cursor for postings file and performs random access using 'seek(offset)' to read each term's postings list when needed. 
the top 10 documents ranked by decreasing cosine similarity, with cosine similarites ranked by increasing 'doc_id'
if there are less than 10 or 10 documents, same logic will apply

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

`index.py` - builds the dictionary and postings files.
`search.py` - ranks queries using lnc.ltc cos similarity with disk-seek postings access.
`dictionary.txt` - pickled dictionary mapping 'term -> (offset, df)' plus metadata ('__doc_lengths__', '__doc_count__').
`postings.txt` - binary postings lists stored on disk as '[df][(doc_id, tf)...]' for each term.
`README.txt`

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0000000X, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Gilligan's Island Rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==
school/cs3245/homework-2's code for tokenization, casefolding, and stemming
- NLTK documentation (tokenization, Porter stemmer): https://www.nltk.org/
- Python docs: pickle (https://docs.python.org/3/library/pickle.html), struct (https://docs.python.org/3/library/struct.html).

CS3245 lecture notes for lnc.ltc weighting scheme