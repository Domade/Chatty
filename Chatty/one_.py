import spacy
import sys

#pip install spacy
#python -m spacy download en_core_web_sm

# Load a pre-trained English model from spaCy
nlp = spacy.load('en_core_web_sm')

# Checking and updating descriptors
def add_descriptor(word):
    if word not in descriptors:
        descriptors.append(word)
        # Save descriptors to a file
        with open('descriptors.txt', 'w') as f:
            for descriptor in descriptors:
                f.write(f"{descriptor}\n")

# Load descriptors from a file if exists
try:
    with open('descriptors.txt', 'r') as f:
        descriptors = f.read().splitlines()
except FileNotFoundError:
    descriptors = []

nouns = ['dog', 'cat', 'mouse', 'house', 'car']
verbs = ['runs', 'jumps', 'sleeps', 'drives', 'sits']
conjunctions = ['and', 'or', 'but', 'because', 'if', 'while', 'although']

# Existing binary search function
# ...
# Assume binary_search function is defined above

while True:
    text = input("Enter the text that you want to check: ")
    if text.lower() == 'quit':
        sys.exit()  # Terminate the program immediately

    words = text.split()  # Split the input text into individual words
    doc = nlp(text)  # Process the text with spaCy

    # Reset 'cheat' flag for the current iteration
    cheat = False

    # Check each word using spaCy's POS tagger
    for token in doc:
        # If an adjective (descriptor) is found, check it against our current list
        if token.pos_ == 'ADJ':
            word = token.text.lower()
            if word not in descriptors:
                add_descriptor(word)
            cheat = True
            print("Descriptor found:", word)
            break
    
    # Check for nouns, verbs, and conjunctions against the predefined lists
    for word in words:
        if binary_search(nouns, word.lower()) != -1 or binary_search(verbs, word.lower()) != -1 or \
           binary_search(conjunctions, word.lower()) != -1:
            cheat = True
            print("Noun, verb, or conjunction found.")
            break

    if not cheat:
        print("What do you mean?")

    # Continue with the rest of your program...
    # ...
