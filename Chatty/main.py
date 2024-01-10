# create  words.json and learned_actions.json in main folder.
# run python main.py
# Import necessary libraries
import sys
import random
import json
import logging
import tkinter as tk
from tkinter import messagebox
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
      global positive_words, negative_words
      global nouns, verbs, descriptors, conjunctions
      nouns = loaded_words.get('nouns', [])
      verbs = loaded_words.get('verbs', [])
      descriptors = loaded_words.get('descriptors', [])
      conjunctions = loaded_words.get('conjunctions', [])
      positive_words = loaded_words.get('positive_words', [])
      negative_words = loaded_words.get('negative_words', [])
  except FileNotFoundError:
    # Return empty lists if the file doesn't exist
    nouns = []
    verbs = []
    descriptors = []
    conjunctions = []
    positive_words = []
    negative_words = []

# Load words at the beginning of the program
load_words()
# Predefined words
greetings = [
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening"
]
farewells = ["bye", "goodbye", "see you later", "farewell"]
# Initialize a global dictionary to store learned actions
learned_actions = {}

# Function to save learned actions to a file
def learn_action(is_positive, action):
  category = "positive" if is_positive else "neutral"  # Changed from "negative" to "neutral"
  if category not in learned_actions:
    learned_actions[category] = []

  if action not in learned_actions[category]:
    learned_actions[category].append(action)
    with open('learned_actions.json', 'w') as la:
      json.dump(learned_actions, la)

# Function to add sentiment words to the list
def manage_sentiment_words(command, sentiment, word):
  global positive_words, negative_words
  sentiment_list = positive_words if sentiment == 'positive' else negative_words

  # Check if the word should be added
  if command == 'add' and word not in sentiment_list:
    sentiment_list.append(word)
    logging.info(f"Added word '{word}' to {sentiment} sentiment list.")
    print(f"Added word '{word}' to {sentiment} sentiment list.")
    save_words()
  elif command == 'remove' and word in sentiment_list:
    sentiment_list.remove(word)
    logging.info(f"Removed word '{word}' from {sentiment} sentiment list.")
    print(f"Removed word '{word}' from {sentiment} sentiment list.")
    save_words()
  else:
    print(
        f"Word '{word}' is already in the {sentiment} sentiment list or cannot be found."
    )

# Simplified sentiment analysis function
def get_sentiment(text):
  if any(word in text.lower() for word in positive_words):
    return "positive"
  elif any(word in text.lower() for word in negative_words):
    return "neutral"  # Changed from "negative" to "neutral"
  else:
    return "neutral"  # Changed from "undetermined" to "neutral"

# Modified get_response function with simplified sentiment analysis
def get_response(text):
  # Check for greeting and farewells
  if any(greeting in text.lower() for greeting in greetings):
    return f"{random.choice(greetings).capitalize()}! How can I help you today?"
  elif any(farewell in text.lower() for farewell in farewells):
    return f"{random.choice(farewells).capitalize()}! Have a great day!"
  # Simplified sentiment analysis implementation
  sentiment = get_sentiment(text)
  if sentiment == "positive":
    suggested_action = "This is a positive response action."
    learn_action(True, suggested_action)
  else:  # Changed from separate `elif` for negative to `else` for neutral
    suggested_action = "Sentiment is neutral. Noted but no action taken."
    learn_action(False, suggested_action)  # Changed to false since neutral is treated as such
  logging.info(f"Suggested Action: {suggested_action}")  # Log the AI's action
  print(f"Suggested Action: {suggested_action}")
  return suggested_action

# Function to handle button click
def on_submit():
  user_text = text_entry.get()
  response = get_response(user_text)
  messagebox.showinfo("Response", response)

# TKinter popup creation
def create_popup():
  root = tk.Tk()
  root.title("Text Input")
  tk.Label(root, text="Enter your text:").pack()
  global text_entry
  text_entry = tk.Entry(root, width=50)
  text_entry.pack()
  submit_button = tk.Button(root, text="Submit", command=on_submit)
  submit_button.pack()
  root.mainloop()

if __name__ == "__main__":
  # Create the popup only if this is the main module being run
  create_popup()