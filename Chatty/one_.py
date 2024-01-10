# pip install spacy
# python -m spacy download en_core_web_sm
# pip install nltk
# python -m nltk.downloader vader_lexicon

# Import necessary libraries
import spacy
import sys
import random
import json
import logging

from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
def get_sentiment(text):
    score = sia.polarity_scores(text)
    positive_score = score['pos']
    return positive_score > 0.1  # Threshold for positive sentiment, adjustable based on requirements.


# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

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

# Load words at the beginning of the program
nouns, verbs, descriptors, conjunctions = load_words()

# Predefined words
greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
farewells = ["bye", "goodbye", "see you later", "farewell"]

# Now modify the existing get_response function within 'main.py':
def get_response(text):
    # Your existing greeting and farewell checks would go here
    # Now, include the sentiment check to determine the response
    is_action_good = get_sentiment(text)
    suggested_action = "This is the default suggested action."
    if is_action_good:
        response = "Action seems good!"
        suggested_action = "This is a positive suggested action."
    else:
        response = "Action might not be good."
        suggested_action = "This is a negative suggested action."
    print(f"Suggested Action: {suggested_action}")
    confirmation = input("Is this a good action? (yes/no): ").strip().lower()
    feedback = ""
    if confirmation == 'yes':
        feedback = "You confirmed that this is a good action."
        # Implement logic to remember this feedback
    elif confirmation == 'no':
        feedback = "You indicated that this is not a good action."
        # Implement logic to remember this feedback
    else:
        feedback = "Invalid response. Please respond with 'yes' or 'no'."
    print(feedback)
    return response  # The function now returns the response based on sentiment
# Function to add a word to a list if it's not already present, using lemmatization
def add_to_list(word, word_list, pos):
    lemma = nlp(word)[0].lemma_
    if lemma not in (nlp(w)[0].lemma_ for w in word_list):
        word_list.append(word)
        logging.info(f"Added word '{word}' to {pos} list.")
        print(f"Added word '{word}' to {pos} list.")
    else:
        print(f"Word '{word}' already in list.")

# Function to manage word lists
def manage_words(command, word, pos):
    global nouns, verbs, descriptors, conjunctions
    word_lists = {
        'noun': nouns,
        'verb': verbs,
        'descriptor': descriptors,
        'conjunction': conjunctions
    }
    if command == 'add':
        add_to_list(word, word_lists[pos], pos)
        save_words()  # Save after manual word addition
    elif command == 'remove':
        if word in word_lists[pos]:
            word_lists[pos].remove(word)
            logging.info(f"Removed word '{word}' from {pos} list.")
            print(f"Removed word '{word}' from {pos} list.")
            save_words()  # Save after manual word removal
    print(word_lists[pos])  # Display updated list

# Main loop for the program
while True:
    text = input("\nEnter text (or type 'manage' to add/remove words): ")

    if text.lower() == 'quit':
        save_words()  # Save words before quitting
        sys.exit()
    elif text.lower() == 'manage':
        command = input("Enter command (add/remove): ").lower()
        pos = input("Enter part of speech (noun/verb/descriptor/conjunction): ").lower()
        word = input("Enter the word: ")
        manage_words(command, word, pos)
    else:
        # Process user input text and get a response
        get_response(text)

  # Initialize a global dictionary to store learned actions
  learned_actions = {"positive": [], "negative": []}
  def learn_action(is_positive, action):
      category = "positive" if is_positive else "negative"
      if action not in learned_actions[category]:
          learned_actions[category].append(action)
      with open('learned_actions.json', 'w') as la:
          json.dump(learned_actions, la)
  def load_learned_actions():
      try:
          with open('learned_actions.json', 'r') as la:
              return json.load(la)
      except FileNotFoundError:
          return {"positive": [], "negative": []}
  # Load learned actions at the beginning of the program
  learned_actions = load_learned_actions()
  # Modify get_response to use learned actions
  def get_response(text):
      # Check for greeting and farewells
      if any(greeting in text.lower() for greeting in greetings):
          return f"{random.choice(greetings).capitalize()}! How can I help you today?"
      elif any(farewell in text.lower() for farewell in farewells):
          return f"{random.choice(farewells).capitalize()}! Have a great day!"

      # Sentiment analysis and response
      is_action_good = get_sentiment(text)
      suggested_action = "This is the default suggested action."
      if is_action_good:
          suggested_action = random.choice(learned_actions["positive"]) if learned_actions["positive"] else "This is a positive suggested action."
      else:
          suggested_action = random.choice(learned_actions["negative"]) if learned_actions["negative"] else "This is a negative suggested action."

      print(f"Suggested Action: {suggested_action}")
      confirmation = input("Is this a good action? (yes/no): ").strip().lower()

      if confirmation == 'yes':
          learn_action(is_action_good, suggested_action)
          feedback = "You confirmed that this is a good action."
      elif confirmation == 'no':
          learn_action(not is_action_good, suggested_action)
          feedback = "You indicated that this is not a good action."
      else:
          feedback = "Invalid response. Please respond with 'yes' or 'no'."

      logging.info(feedback) # Log user feedback
      print(feedback)
      return suggested_action
  # ... (rest of the existing code)