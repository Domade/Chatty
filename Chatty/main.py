# create words.json and learned_actions.json in main folder.
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


# Simplified sentiment analysis function
def get_sentiment(text):
  # Load global sentiment word lists
  global positive_words, negative_words, swear_words
  score = 0
  contains_swear = False
  # First, check for swear words to set a flag
  for word in text.lower().split():
    if contains_swear:  # Skip subsequent processing if a swear word is already found
      break
    if word in swear_words:
      contains_swear = True
  # If no swear word is found, calculate sentiment score
  if not contains_swear:
    for word in text.lower().split():
      if word in positive_words:
        score = min(score + 1, 8)  # Ensure score does not exceed 8
      elif word in negative_words:
        score = max(score - 1, -8)  # Ensure score does not go below -8
  # Return the proper sentiment result
  if contains_swear:
    return "swear", [9]
  else:
    if score > 0:
      return "positive", [score]
    elif score < 0:
      return "negative", [score]
    else:
      return "neutral", [0]


# Function to get word type scores
def get_word_type_scores(text):
  global nouns, verbs, descriptors, conjunctions
  words = text.lower().split()
  scores = []
  for word in words:
    if word in verbs:
      scores.append(min(verbs.index(word) + 1, 3))
    elif word in nouns:
      scores.append(min(nouns.index(word) + 1, 4))
    elif word in descriptors:
      scores.append(min(descriptors.index(word) + 1, 8))
    elif word in conjunctions:
      scores.append(0)
    elif word in swear_words:
      scores.append(9)
    else:
      scores.append(0)
  return scores


# Function to compare sentiment and word type analyses
def analyze_text(text):
  sentiment_result, sentiment_scores = get_sentiment(text)
  word_type_scores = get_word_type_scores(text)
  return sentiment_result, sentiment_scores, word_type_scores


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
              loaded_words.get('descriptors', []), loaded_words.get('conjunctions', []),
              loaded_words.get('positive_words', []), loaded_words.get('negative_words', []),
              loaded_words.get('swear_words', []))  # Adding swear_words to the returned tuple
  except FileNotFoundError:
    return [], [], [], [], [], [], []  # Return empty lists if the file doesn't exist


# Load words at the beginning of the program
# Update the global lists including the sentiment lists and swear_words list
nouns, verbs, descriptors, conjunctions, positive_words, negative_words, swear_words = load_words()
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
  if is_positive:
    logging.info(f"User indicated positive sentiment: {action}")
    print(f"User indicated positive sentiment: {action}")
  else:
    logging.info(f"User indicated negative sentiment: {action}")
    print(f"User indicated negative sentiment: {action}")


# Function to manage word lists
def manage_words(command, word, pos):
  global nouns, verbs, descriptors, conjunctions, positive_words, negative_words
  word_lists = {
      'noun': nouns,
      'verb': verbs,
      'descriptor': descriptors,
      'conjunction': conjunctions,
      'positive': positive_words,
      'negative': negative_words
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


# Function to handle button click
def on_submit():
  user_text = text_entry.get()
  response, sentiment_scores, word_type_scores = analyze_text(user_text)
  print("Sentiment Scores:", sentiment_scores, "Word Type Scores:", word_type_scores)
  display_response = get_response(user_text)
  messagebox.showinfo("Response", display_response)


# Modify get_response function to not include sentiment and word type scores in the response
def get_response(text):
  sentiment_result, sentiment_scores, word_type_scores = analyze_text(text)
  if sentiment_result == "swear":
    logging.warning(f"Swear word detected: {text}")
    return "I'm unable to respond to that."
  if any(greeting in text.lower() for greeting in greetings):
    return f"{random.choice(greetings).capitalize()}! How can I help you today?"
  elif any(farewell in text.lower() for farewell in farewells):
    return f"{random.choice(farewells).capitalize()}! Have a great day!"
  else:
    response = "How can I assist you?"
    if sentiment_result == "positive":
      suggested_action = "This is a positive response action."
      learn_action(True, suggested_action)
      response = f"{suggested_action} {response}"
    elif sentiment_result == "negative":
      suggested_action = "This is a negative response action."
      learn_action(False, suggested_action)
      response = f"{suggested_action} {response}"
  return response


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
  create_popup()