This is the README file for A0252480J's submission
Email: e0958068@u.nus.edu

== Python Version ==

I'm using Python Version <3.14.2> for
this assignment.

== General Notes about this assignment ==

Inspecting the inputs, I split the sentences up into [first_word] and [remaining_sentence].
Splitting the languages into its own dictionaries, I keep a count of four-gram (key) : counts (value).
A masterlist of all four-grams across languages is filled to facilitate add-one smoothing.
Add-one smoothed count is converted into probability, dividing it by total count per language.
Final collection is dictionary {languages { probabilities }}
When determining language, log(probability) is added up to form a score, and the highest score is the predicted language.
If the scores are all the same or zero, language is alien.
Algorithm to test threshold of probability before declaring it as "Other" or confirming it as a language is not implemented as I am unsure.

Algorithms used:
1. 4-gram language modeling
2. add-one (laplace) smoothing

Important Considerations:
1. character-level four-grams
2. include spaces and punctuations

== Files included with this submission ==

README.txt, overview of program and algorithms used
build_test_LM.py, source code

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0252480J, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==

For dictionary: https://docs.python.org/3/tutorial/datastructures.html
For max function: https://docs.python.org/3/library/functions.html#max
