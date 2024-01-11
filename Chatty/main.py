# create words.json and learned_actions.json in main folder.
# run python main.py
# Import necessary libraries
import sys
import json
import logging
import os
import tkinter as tk
from tkinter import messagebox
import threading


# Initialize logging
logging.basicConfig(filename='app.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')
class GlobalState:
  def __init__(self):
    self.word_types = {
        'nouns': [], 'verbs': [], 'descriptors': [], 'conjunctions': [],
        'positive_words': [], 'negative_words': [], 'swear_words': [],
        'greetings': [], 'farewells': []
    }
    self.learned_actions = {'positive': [], 'negative': [], 'neutral': []}
    self.action_buffer = []

  def add_word(self, word_type, word):
    if word_type in self.word_types and word not in self.word_types[word_type]:
      self.word_types[word_type].append(word)
      self.save_words_to_file('words.json')

  def get_word_by_type(self, word_type):
    return self.word_types.get(word_type, [])

  def set_words_by_type(self, word_type, words):
    if word_type in self.word_types:
      self.word_types[word_type] = words
      self.save_words_to_file('words.json')

  def update_learned_actions(self, sentiment, phrase):
    if phrase not in self.learned_actions[sentiment]:
      self.learned_actions[sentiment].append(phrase)
      self.action_buffer.append((sentiment, phrase))

  def save_state(self):
    self.save_words_to_file('words.json')
    self.save_learned_actions_to_file('learned_actions.json')

  def load_words_from_file(self, file_path):
    try:
      with open(file_path, 'r') as file:
        words_data = json.load(file)
        for word_type in self.word_types:
          self.word_types[word_type] = words_data.get(word_type, [])
      logging.info("Words loaded successfully.")
    except Exception as e:
      logging.error(f"Failed to load words: {e}")
      raise

  def save_words_to_file(self, file_path):
    try:
      with open(file_path, 'w') as file:
        json.dump(self.word_types, file, indent=2)
      logging.info("Words saved successfully.")
    except Exception as e:
      logging.error(f"Failed to save words: {e}")
      raise

  def load_learned_actions_from_file(self, file_path):
    try:
      with open(file_path, 'r') as file:
        self.learned_actions = json.load(file)
      logging.info("Learned actions loaded successfully.")
    except FileNotFoundError:
      logging.info("No learned actions file found. Continuing with empty actions.")
    except Exception as e:
      logging.error(f"Failed to load learned actions: {e}")
      raise

  def save_learned_actions_to_file(self, file_path):
    try:
      with open(file_path, 'w') as file:
        json.dump(self.learned_actions, file, indent=2)
      self.action_buffer.clear()
      logging.info("Learned actions saved successfully.")
    except Exception as e:
      logging.error(f"Failed to save learned actions: {e}")
      raise



def get_sentiment(text, state):  # Accept state as an argument
      score = 0
      contains_swear = False
      for word in text.lower().split():
        if word in state.get_word_by_type('swear_words'):
          contains_swear = True
          break
      if not contains_swear:
        for word in text.lower().split():
          if word in state.get_word_by_type('positive_words'):
            score = min(score + 1, 8)  # Ensure score does not exceed 8
          elif word in state.get_word_by_type('negative_words'):
            score = max(score - 1, -8)  # Ensure score does not go below -8
      if contains_swear:
        return "swear", [9]
      else:
        if score > 0:
          return "positive", [score]
        elif score < 0:
          return "negative", [score]
        else:
          return "neutral", [0]

def get_word_type_scores(text, state):  # Accept state as an argument
      word_types = state.word_types
      words = text.lower().split()
      scores = []
      for word in words:
        # ... existing conditions
        scores.append(0)
      return scores  # Correctly dedented to align with the for loop

def analyze_text(text, state):  # Accept state as an argument
  sentiment_result, sentiment_scores = get_sentiment(text, state)  # Pass state to the function call
  word_type_scores = get_word_type_scores(text, state)  # Pass state to the function call
  return sentiment_result, sentiment_scores, word_type_scores


def learn_action(is_positive, user_text, state):
  category = "positive" if is_positive else "negative"
  state.update_learned_actions(category, user_text)
  state.save_learned_actions_to_file('learned_actions.json')

def create_user_decide_popup(user_text, state):
  def close_popup():
      popup.destroy()
  def handle_positive_sentiment():
      learn_action(True, user_text, state)  # Pass state to the function call
      close_popup()

    def check_learned_phrases(text, state):

      learned_phrases = state.learned_actions  # use the in-memory data

      for sentiment, phrases in learned_phrases.items():
        if text in phrases:
          return sentiment
      return None

    def get_response(text, state):
    
      try:
        sentiment_result, sentiment_scores, word_type_scores = analyze_text(
            text, state)
        learned_sentiment = check_learned_phrases(text, state)
        if any(greeting in text.lower() for greeting in state.get_word_by_type('greetings')):
          response = f"{random.choice(state.get_word_by_type('greetings')).capitalize()}! How can I help you today?"
        elif any(farewell in text.lower() for farewell in state.get_word_by_type('farewells')):
          response = f"{random.choice(state.get_word_by_type('farewells')).capitalize()}! Have a great day!"
        # Handle swear words specifically
        elif sentiment_result == "swear":
          response = "I'm unable to respond to that."
        else:
          # Provide a generic response for all other cases
          response = "How can I assist you?"
        messagebox.showinfo("Response", response)
        # Ask the user if they need to clarify the sentiment
        if learned_sentiment != "positive":
          answer = messagebox.askyesno(
              "Clarification",
              "Do you need to clarify the sentiment of the phrase?")
          if answer:
              create_user_decide_popup(text, state)
          else:
              if sentiment_result in ["positive", "negative"]:
                  learn_action(sentiment_result == "positive", text, state)
        return response
      except Exception as e:
        logging.error(f"An error occurred in get_response: {e}")
      return "I'm sorry, but an error occurred while generating a response."

    def response_results(sentiment_result, sentiment_scores, word_type_scores):
      results = f"Sentiment: {sentiment_result}, " \
            f"Sentiment Scores: {sentiment_scores}, " \
            f"Word Type Scores: {word_type_scores}"
      print(results)

    def create_sentiment_buttons(user_text):

      def close_popup():
        popup.destroy()

      def create_sentiment_buttons(user_text, state):
        learn_action(True, user_text, state)

      popup = tk.Tk()
      popup.title("Sentiment Undetermined")
      tk.Label(popup, text="Unable to determine sentiment.").pack()
      tk.Button(popup,
                text="Sentiment is Positive",
                command=handle_positive_sentiment).pack()
      tk.Button(popup, text="Sentiment is Negative",
                command=close_popup).pack()
      popup.mainloop()

      popup.destroy()

def on_submit(state, text_entry):  # Accept state and text_entry as arguments
  try:
      user_input = text_entry.get()
      threading.Thread(target=lambda: get_response_and_save(user_input, state),  
                       # Pass state to the function call
                       daemon=True).start()
  except Exception as e:
      logging.error(f"An error occurred in on_submit: {e}")
      messagebox.showerror("Error", str(e))

    def get_response_and_save(user_input, state):
      # Accept state as an argument
      response = get_response(user_input, state)  # Pass state to the function call
      messagebox.showinfo("Response", response)
      
      state.save_learned_actions_to_file(
          'learned_actions.json')  # save any updated learned actions

def create_popup(state):  # Accept state as an argument
  popup = tk.Toplevel()  # Use Toplevel instead of a new Tk instance
  popup.title("Text Input")
  text_entry = tk.Entry(popup, width=50)
  text_entry.pack()
  submit_button = tk.Button(popup, text="Submit", command=lambda: on_submit(state, text_entry))
  # Pass state and text_entry
  submit_button.pack()



def main():
  # This function should initiate the main application window and loop
  root = tk.Tk()
  # ...
  # Setup the rest of your Tkinter widgets here before starting the mainloop

  # Create a GlobalState instance and load data from files
  state = GlobalState()
  create_popup(state)
  
  try:
      state.load_words_from_file('words.json')
      state.load_learned_actions_from_file('learned_actions.json')
  
      root.mainloop()



# Place the if __name__ == "__main__": block at the bottom, correctly indented
if __name__ == "__main__":
  main()  # This will start your main application
