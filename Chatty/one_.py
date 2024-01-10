
# create  words.json and learned_actions.json in main folder.
# run python main.py

# Import necessary libraries
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
logging.basicConfig(filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')


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
      return (loaded_words.get('nouns', []), loaded_words.get('verbs', []),
              loaded_words.get('descriptors',
                               []), loaded_words.get('conjunctions', []))
  except FileNotFoundError:
    return [], [], [], []  # Return empty lists if the file doesn't exist


# Load words at the beginning of the program
nouns, verbs, descriptors, conjunctions = load_words()

# Predefined words
greetings = [
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening"
]
farewells = ["bye", "goodbye", "see you later", "farewell"]

# Initialize a global dictionary to store learned actions
learned_actions = {"positive": [], "negative": []}


# Function to save learned actions to a file
def learn_action(is_positive, action):
  category = "positive" if is_positive else "negative"
  if action not in learned_actions[category]:
    learned_actions[category].append(action)

  with open('learned_actions.json', 'w') as la:
    json.dump(learned_actions, la)


# Function to load learned actions from a file
def load_learned_actions():
  try:
    with open('learned_actions.json', 'r') as la:
      return json.load(la)
  except FileNotFoundError:
    return {"positive": [], "negative": []}


# Load learned actions at the beginning of the program
learned_actions = load_learned_actions()


# Consolidated get_response function
def get_response(text):
  # Check for greeting and farewells
  if any(greeting in text.lower() for greeting in greetings):
    return f"{random.choice(greetings).capitalize()}! How can I help you today?"
  elif any(farewell in text.lower() for farewell in farewells):
    return f"{random.choice(farewells).capitalize()}! Have a great day!"

  # Attempt to use learned actions based on sentiment
  is_action_good = get_sentiment(text)
  suggested_action = "This is the default suggested action."
  if is_action_good:
    suggested_action = random.choice(
        learned_actions["positive"]) if learned_actions[
            "positive"] else "This is a positive suggested action."
  else:
    suggested_action = random.choice(
        learned_actions["negative"]) if learned_actions[
            "negative"] else "This is a negative suggested action."

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

  logging.info(feedback)  # Log user feedback
  print(feedback)
  return suggested_action


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
    if word not in word_lists[pos]:
      word_lists[pos].append(word)
      logging.info(f"Added word '{word}' to {pos} list.")
      print(f"Added word '{word}' to {pos} list.")
      save_words()  # Save after manual word addition
    else:
      print(f"Word '{word}' already in list.")
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
    pos = input(
        "Enter part of speech (noun/verb/descriptor/conjunction): ").lower()
    word = input("Enter the word: ")
    manage_words(command, word, pos)
  else:
    # Process user input text and get a response
    get_response(text)