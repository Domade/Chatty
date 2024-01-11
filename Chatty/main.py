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
import signal
import threading  # Import threading for background tasks

# Initialize logging
logging.basicConfig(filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')


def robust_exit_handler(signum, frame):
  save_learned_actions_from_buffer()  # Save buffer to file before exiting
  save_words()  # Save word lists when program is exiting
  logging.info("Program exited gracefully.")
  sys.exit(0)


# Register the robust exit handler for various exit signals
for s in [signal.SIGINT, signal.SIGTERM, signal.SIGABRT]:
  signal.signal(s, robust_exit_handler)


# Function to load words from a file
def load_words():
  try:
    with open('words.json', 'r') as f:
      loaded_words = json.load(f)
      general_words = (
          loaded_words.get('nouns', []),
          loaded_words.get('verbs', []),
          loaded_words.get('descriptors', []),
          loaded_words.get('conjunctions', []),
      )
      sentiment_words = (
          loaded_words.get('positive_words', []),
          loaded_words.get('negative_words', []),
          loaded_words.get('swear_words', []),  # Initialize swear_words list
          loaded_words.get('greetings', []),
          loaded_words.get('farewells', []))
      return general_words, sentiment_words
  except Exception as e:
    logging.error(f"Failed to load words: {e}")
  messagebox.showerror("Error", "Failed to load words from file.")
  return ((), ())


# Now that the function is defined, call load_words to initialize your word lists
general_words, sentiment_words = load_words()
nouns, verbs, descriptors, conjunctions = general_words
positive_words, negative_words, swear_words, greetings, farewells = sentiment_words

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
  try:
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
  except Exception as e:
    logging.error(f"Failed to save learned actions: {e}")


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
    popup.after(0, close_popup)

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
        messagebox.showinfo(
            "Sentiment Decision",
            "The sentiment is negative and will not be saved.")
      popup.after(
          0, close_popup)  # Schedule the popup to close in the main thread

    popup = tk.Tk()
    popup.title("Your Input is Needed")

    tk.Label(popup, text="We need your help with the sentiment.").pack()
    tk.Button(popup,
              text="This is Positive",
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


# Previous sections of the code remain the same up to this point ...


# Modified get_response function to correctly handle neutral sentiment
# Modified get_response function to correctly handle neutral sentiment
def get_response(text):
  try:
    sentiment_result, sentiment_scores, word_type_scores = analyze_text(text)
    learned_sentiment = check_learned_phrases(text)

    # Prioritize learned sentiment but prompt user if it's neutral and learned
    if learned_sentiment == "neutral":
      create_user_decide_popup(text)
      return "Please decide on the sentiment of the phrase."

    # If the sentiment is neutral and not learned, or learned as positive or negative, prompt the user
    elif sentiment_result == "neutral" or learned_sentiment in ("positive",
                                                                "negative"):
      if learned_sentiment:
        response = f"Learned response with a {learned_sentiment} sentiment."
        messagebox.showinfo("Learned Sentiment", response)
      else:
        create_user_decide_popup(text)
        return "Please decide on the sentiment of the phrase."

    # Learned sentiment takes precedence if it is positive or negative
    elif learned_sentiment in ("positive", "negative"):
      response = f"Learned response with a {learned_sentiment} sentiment."
      messagebox.showinfo("Learned Sentiment", response)
      return response

    # Handle specific cases such as swear words, greetings, farewells
    elif sentiment_result == "swear":
      response = "I'm unable to respond to that."
    elif any(greeting in text.lower() for greeting in greetings):
      response = f"{random.choice(greetings).capitalize()}! How can I help you today?"
    elif any(farewell in text.lower() for farewell in farewells):
      response = f"{random.choice(farewells).capitalize()}! Have a great day!"
    else:
      # General case
      response = "How can I assist you?"

    # Learn and respond if sentiment is either positive or negative
    if sentiment_result == "negative":
      learn_action(False, text)
    elif sentiment_result == "positive":
      learn_action(True, text)

    # Save the learned phrase regardless of sentiment
    save_learned_phrase(text, sentiment_result)
    response_results(sentiment_result, sentiment_scores, word_type_scores)

  except Exception as e:
    logging.error(f"An error occurred in get_response: {e}")
    return "I'm sorry, but an error occurred while generating a response."

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
  global root
  try:
    user_input = text_entry.get()
    # Start the get_response and save operations as a background thread
    threading.Thread(target=lambda: get_response_and_save(user_input),
                     daemon=True).start()
  except Exception as e:
    logging.error(f"An error occurred in on_submit: {e}")
    messagebox.showerror("Error", str(e))


def get_response_and_save(user_input):
  response = get_response(
      user_input)  # This is unchanged from your existing code
  messagebox.showinfo("Response", response)
  save_learned_actions_from_buffer(
  )  # This is unchanged from your existing code


# TKinter popup creation
def create_popup():
  global root
  root = tk.Tk()  # Assign root to global for proper termination in on_submit
  root.title("Text Input")
  tk.Label(root, text="Enter your text:").pack()
  global text_entry
  text_entry = tk.Entry(root, width=50)
  text_entry.pack()
  # Update the submit button to not call on_submit directly
  submit_button = tk.Button(root, text="Submit", command=on_submit)
  submit_button.pack()
  root.mainloop()


# At the end of your script, add the definition for on_program_exit
def on_program_exit():
  try:
    # ... existing on_program_exit code ...
    pass
  except Exception as e:
    logging.error(f"Failed to save all data on exit: {e}")
  finally:
    print("Program exiting...")


# Main entry point
if __name__ == "__main__":
  try:
    create_popup()
  except tk.TclError:
    pass
  finally:
    #robust_exit_handler(None, None)  # Trigger the robust exit handler
    pass  # Add an indented block of code here
