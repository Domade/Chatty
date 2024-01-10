#pip install spacy
#python -m spacy download en_core_web_sm

# Import necessary libraries
import spacy
import sys
import random
import json
# Function to save words to a file
def save_words():
    with open('words.json', 'w') as f:
        words_to_save = {
            'nouns': nouns,
            'verbs': verbs,
            'descriptors': descriptors,
            'conjunctions': conjunctions
        }
        json.dump(words_to_save, f)
# Function to load words from a file
def load_words():
    try:
        with open('words.json', 'r') as f:
            loaded_words = json.load(f)
            return (
                loaded_words.get('nouns', []),
                loaded_words.get('verbs', []),
                loaded_words.get('descriptors', []),
                loaded_words.get('conjunctions', [])
            )
    except FileNotFoundError:
        return [], [], [], []  # Return empty lists if the file doesn't exist
# Load the words at the beginning of your program
nouns, verbs, descriptors, conjunctions = load_words()
# ... rest of your program ...
# Save the words at the end of your program or after updating any list
save_words()

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define lists with predefined words
greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
farewells = ["bye", "goodbye", "see you later", "farewell"]
wellbeing = ["how are you", "how's it going", "what's up"]
weather_statements = ["weather", "rain", "sunny", "cloudy", "hot", "cold"]
nouns = ['dog', 'cat', 'mouse', 'house', 'car']
verbs = ['runs', 'jumps', 'sleeps', 'drives', 'sits']
descriptors = ['quick', 'lazy', 'sleepy', 'happy', 'sad']
conjunctions = ['and', 'or', 'but', 'because', 'if', 'while', 'although']

# Function to process and respond to the input text
def get_response(text, doc):
    text_lower = text.lower()
    # Check for greetings
    if any(greet in text_lower for greet in greetings):
        return random.choice(["Hello!", "Hi there!", "Hey!"])
    # Check for farewells
    if any(farewell in text_lower for farewell in farewells):
        return random.choice(["Goodbye!", "See you later!", "Farewell then!"])
    # Check for wellbeing questions
    if any(well in text_lower for well in wellbeing):
        return "I'm just a program, but I'm functioning properly. How about you?"
    # Check for weather related conversation
    if any(weather in text_lower for weather in weather_statements):
        return "I don't have the latest weather updates but I hope it's pleasant for you!"
    # Default response
    return "That's interesting. Tell me more!"

# Function to add a word to a list if it's not already present
def add_to_list(word, word_list):
    if word not in word_list:
        word_list.append(word)

# Main loop for the program
while True:
    text = input("Enter the text that you want to check: ")
    if text.lower() == 'quit':
        sys.exit()
    words = text.split()
    cheat = False
    for word in words:
        # Convert word to lowercase
        word_lower = word.lower()
        if word_lower in (w.lower() for w in descriptors) or \
           word_lower in (w.lower() for w in nouns) or \
           word_lower in (w.lower() for w in verbs) or \
           word_lower in (w.lower() for w in conjunctions):
            print("Descriptor, noun, verb, or conjunction found.")
            cheat = True
            break

    if not cheat:
        doc = nlp(text)
        for token in doc:
            if token.pos_ == 'NOUN' and token.text not in nouns:
                add_to_list(token.text, nouns)
            elif token.pos_ == 'VERB' and token.text not in verbs:
                add_to_list(token.text, verbs)
            elif token.pos_ == 'ADJ' and token.text not in descriptors:
                add_to_list(token.text, descriptors)
            elif token.pos_ == 'CONJ' and token.text not in conjunctions:
                add_to_list(token.text, conjunctions)

        response = get_response(text, doc)
        print(response)