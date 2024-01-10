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


# Simplified sentiment analysis function
def get_sentiment(text):
  positive_words = ['good', 'great', 'awesome', 'happy', 'love']
  negative_words = ['bad', 'sad', 'terrible', 'hate', 'unhappy']
  swear_words = ['shit', 'damn', 'hell']  # Add your list of swear words here
  score = 0
  # Check each word in the text
  for word in text.lower().split():
    if word in swear_words:
      return "swear", [
          9
      ]  # Return the detected swear sentiment and the corresponding score as an array
    if word in positive_words:
      score += 1
    elif word in negative_words:
      score -= 1
  if score > 0:
    return "positive", [score]
  elif score < 0:
    return "negative", [score]
  else:
    return "neutral", [0]


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
  if is_positive:
    # Your code to handle the positive sentiment
    logging.info(f"User indicated positive sentiment: {action}")
    print(f"User indicated positive sentiment: {action}")
    # Optionally save this action or increment some counter etc.


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


# Function to add sentiment words to the list
def manage_sentiment_words(command, sentiment, word):
  global positive_words, negative_words
  sentiment_list = positive_words if sentiment == 'positive' else negative_words

  # Check if the word should be added
  if command == 'add' and word not in sentiment_list:
    sentiment_list.append(word)
    logging.info(f"Added word '{word}' to {sentiment} sentiment list.")
    print(f"Added word '{word}' to {sentiment} sentiment list.")
  elif command == 'remove' and word in sentiment_list:
    sentiment_list.remove(word)
    logging.info(f"Removed word '{word}' from {sentiment} sentiment list.")
    print(f"Removed word '{word}' from {sentiment} sentiment list.")
  else:
    print(
        f"Word '{word}' is already in the {sentiment} sentiment list or cannot be found."
    )
  # Save the lists to the file system
  save_sentiment_words(sentiment_list, sentiment)


def save_sentiment_words(sentiment_words, sentiment):
  try:
    with open('words.json', 'r+') as f:
      words = json.load(f)
      if sentiment == 'positive':
        words['positive_words'] = sentiment_words
      else:
        words['negative_words'] = sentiment_words
      f.seek(0)
      f.truncate()
      json.dump(words, f)
  except FileNotFoundError:
    print("The words.json file does not exist. Creating a new one.")
    with open('words.json', 'w') as f:
      words = {'positive_words': [], 'negative_words': []}
      words[sentiment + '_words'] = sentiment_words
      json.dump(words, f)


# Modify load_words function
def load_words():
  try:
    with open('words.json', 'r') as f:
      loaded_words = json.load(f)
      # Include the positive and negative words lists in the return statement
      return (loaded_words.get('nouns', []), loaded_words.get('verbs', []),
              loaded_words.get('descriptors',
                               []), loaded_words.get('conjunctions', []),
              loaded_words.get('positive_words',
                               []), loaded_words.get('negative_words', []))
  except FileNotFoundError:
    return [], [], [], [], [], [
    ]  # Return empty lists if the file doesn't exist


# Update the global lists including the sentiment lists
nouns, verbs, descriptors, conjunctions, positive_words, negative_words = load_words(
)


# Modified get_response function with simplified sentiment analysis
def get_response(text):
  # Split the text and print indices for all sentiments
  indices = [i for i, _ in enumerate(text.split())]
  print(indices)
  # Check for swear words first
  sentiment, score = get_sentiment(text)
  if sentiment == "swear":
    logging.warning(f"Swear word detected: {text}")
    print(indices + [9])
    return "Do not speak to me that way."

  # Return the detected swear sentiment and the corresponding score

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
  elif sentiment == "negative":
    suggested_action = "This is a negative response action."
    learn_action(False, suggested_action)
  elif sentiment == "undetermined":
    create_sentiment_buttons(text)
    return "Checking sentiment..."
  else:
    suggested_action = "This is a neutral response."
  logging.info(f"Suggested Action: {suggested_action}")  # Log the AI's action
  print(f"Suggested Action: {suggested_action}")
  return suggested_action


# Create TKinter popup to handle undetermined sentiment
def create_sentiment_buttons(user_text):

  def close_popup():
    popup.destroy()

  def handle_positive_sentiment():
    # Here you can handle the positive sentiment, e.g., by saving it somewhere
    learn_action(True, "User indicated positive sentiment.")
    close_popup()

  popup = tk.Tk()
  popup.title("Sentiment Undetermined")
  tk.Label(popup, text="Unable to determine sentiment.").pack()
  tk.Button(popup,
            text="Sentiment is Positive",
            command=handle_positive_sentiment).pack()
  tk.Button(popup, text="Sentiment is Negative", command=close_popup).pack()
  popup.mainloop()


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
