# create words.json and learned_actions.json in main folder.
# run python main.py
# Import necessary libraries
import sys
import random
import json
import logging
import os
import tkinter as tk
from tkinter import messagebox

# Initialize logging
logging.basicConfig(filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')


# Simplified sentiment analysis function
# [...Same as previous...]
# Your other function definitions should be here
# Function to load words from a file
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


# Now that the function is defined, call load_words to initialize your word lists
nouns, verbs, descriptors, conjunctions, positive_words, negative_words = load_words(
)
# Initialize a global dictionary to store learned actions
learned_actions = {"positive": [], "negative": []}
# Create a buffer to prevent direct writing to file for every action
action_buffer = []


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


# Function to save learned phrases
def save_learned_phrase(phrase, sentiment):
  if sentiment == 'negative':
    # Do not save negative sentiments
    return

  file_path = 'learned_phrases.json'
  phrases_data = {}

  # Load current phrases if file exists
  if os.path.isfile(file_path):
    with open(file_path, 'r') as file:
      phrases_data = json.load(file)

  # Check if the phrase has already been learned
  if sentiment in phrases_data and phrase in phrases_data[sentiment]:
    return  # Phrase already learned, do nothing

  # Append new phrase to the appropriate sentiment list
  if sentiment not in phrases_data:
    phrases_data[sentiment] = [phrase]
  else:
    phrases_data[sentiment].append(phrase)

  # Write updated phrases back to the file
  with open(file_path, 'w') as file:
    json.dump(phrases_data, file, indent=2)


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


# Function to save learned actions to a file
# Function to manage learned actions
def learn_action(is_positive, phrase):
  category = "positive" if is_positive else "negative"
  if phrase not in learned_actions[category]:
    learned_actions[category].append(phrase)
    # Append to buffer instead of writing directly to the file
    action_buffer.append((category, phrase))


# Function to save learned actions to file from the buffer
def save_learned_actions_from_buffer():
  if os.path.exists('learned_actions.json'):
    with open('learned_actions.json', 'r') as file:
      learned_actions = json.load(file)
  else:
    learned_actions = {"positive": [], "negative": []}
  # Update learned actions with contents of the buffer
  for category, phrase in action_buffer:
    if phrase not in learned_actions[category]:
      learned_actions[category].append(phrase)
  with open('learned_actions.json', 'w') as file:
    json.dump(learned_actions, file, indent=2)


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


# Modify the create_user_decide_popup function accordingly
def create_user_decide_popup(user_text):

  def close_popup():
    popup.destroy()

  def handle_positive_sentiment():
    save_learned_phrase(user_text, "positive")
    learn_action(True, user_text)
    close_popup()

  def ai_decide_sentiment():
    sentiment_result = get_sentiment(user_text)[0]
    if sentiment_result != "negative":
      create_sentiment_buttons(user_text)
    else:
      messagebox.showinfo("Sentiment Decision",
                          "The sentiment is negative and will not be saved.")
    close_popup()

  popup = tk.Tk()
  popup.title("Your Input is Needed")

  tk.Label(popup, text="We need your help with the sentiment.").pack()

  tk.Button(popup, text="This is Positive",
            command=handle_positive_sentiment).pack()
  tk.Button(popup, text="You Decide", command=ai_decide_sentiment).pack()

  close_button = tk.Button(popup, text="Close", command=close_popup)
  close_button.pack()

  popup.mainloop()


def check_learned_phrases(text):
  try:
    with open('learned_phrases.json', 'r') as file:
      learned_phrases = json.load(file)
      for sentiment, phrases in learned_phrases.items():
        if text in phrases:
          return sentiment
    return None
  except FileNotFoundError:
    # If the file is not found, no phrases have been learned
    return None


# Modified get_response function to print sentiment to the console
def get_response(text):
  sentiment_result, sentiment_scores, word_type_scores = analyze_text(text)

  # Inside get_response function
  learned_sentiment = check_learned_phrases(text)
  if learned_sentiment:
    # Return a response based on the learned sentiment
    return f"Learned response with a {learned_sentiment} sentiment."

  if sentiment_result == "swear":
    logging.warning(f"Swear word detected: {text}")
    print("Swear word detected.")  # Print to console instead of pop-up
    return "I'm unable to respond to that."

  if any(greeting in text.lower() for greeting in greetings):
    response = f"{random.choice(greetings).capitalize()}! How can I help you today?"
  elif any(farewell in text.lower() for farewell in farewells):
    response = f"{random.choice(farewells).capitalize()}! Have a great day!"
  else:
    response = "How can I assist you?"

  # Print sentiment information to console, not included in pop-up
  if sentiment_result == "positive":
    learn_action(True, text)

    print(f"Detected positive sentiment with the statement: {text}")
  elif sentiment_result == "negative":
    suggested_action = "This is a negative response action."
    learn_action(False, suggested_action)
    print(f"Detected negative sentiment with the statement: {text}")

  # Only save phrase if not negative
  if sentiment_result != "negative":
    save_learned_phrase(text, sentiment_result)

  if sentiment_result == "neutral":
    create_user_decide_popup(text)

  # Call response_results here to print the sentiment and word type scores
  response_results(sentiment_result, sentiment_scores, word_type_scores)

  # Response is returned for pop-up without revealing sentiment analysis
  return response


# Function to print the results of the sentiment analysis
def response_results(sentiment_result, sentiment_scores, word_type_scores):
  results = f"Sentiment: {sentiment_result}, " \
            f"Sentiment Scores: {sentiment_scores}, " \
            f"Word Type Scores: {word_type_scores}"
  print(results)


# Create TKinter popup to handle undetermined sentiment
def create_sentiment_buttons(user_text):

  def close_popup():
    popup.destroy()

  def handle_positive_sentiment():
    save_learned_phrase(user_text, "positive")
    learn_action(True, user_text)
    close_popup()

  popup = tk.Tk()
  popup.title("Sentiment Undetermined")
  tk.Label(popup, text="Unable to determine sentiment.").pack()
  tk.Button(popup,
            text="Sentiment is Positive",
            command=handle_positive_sentiment).pack()
  tk.Button(popup, text="Sentiment is Negative", command=close_popup).pack()
  popup.mainloop()


def on_submit():
  user_input = text_entry.get(
  )  # You may need to retrieve and process the text entry from the user
  response = get_response(
      user_input)  # Assuming you have a response function to handle the input
  messagebox.showinfo(
      "Response", response
  )  # Show the response in a messagebox, or feel free to handle differently


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


# Main entry point
if __name__ == "__main__":
  try:
    # Create the popup only if this is the main module being run
    create_popup()
  except tk.TclError:
    # Handle exceptions that may occur when Tkinter isn't available/closed
    pass
  finally:
    on_program_exit()
