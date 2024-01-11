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

      class GlobalState:
        def __init__(self):
            self.learned_actions = {"positive": [], "negative": []}
            self.action_buffer = []
            self.word_types = {
                'nouns': [],
                'verbs': [],
                'descriptors': [],
                'conjunctions': [],
                'positive_words': [],
                'negative_words': [],
                'swear_words': [],
                'greetings': [],
                'farewells': []
            }
            # Removed "pass" since it's unnecessary here

        def add_word(self, word_type, word):
            if word_type in self.word_types and word not in self.word_types[word_type]:
                self.word_types[word_type].append(word)
                self.save_words_to_file('words.json')  
              # Assuming words.json is the file where words are stored

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
          # Save words and learned actions to files
          pass

      # Define more methods to handle the internal logic

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
              self.action_buffer.clear()  # Clear the action buffer after saving
              logging.info("Learned actions saved successfully.")
          except Exception as e:
              logging.error(f"Failed to save learned actions: {e}")
              raise


      ## Simplified sentiment analysis function
      def get_sentiment(text):
        # Use state instance instead of global variables
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

      def get_word_type_scores(text):
      # Use state instance instead of global variables
          word_types = state.word_types
          words = text.lower().split()
          scores = []
          for word in words:
          # ... existing conditions
              scores.append(0)
          return scores  # Correctly dedented to align with the for loop



      # Function to compare sentiment and word type analyses
      def analyze_text(text):
        sentiment_result, sentiment_scores = get_sentiment(text)
        word_type_scores = get_word_type_scores(text)
        return sentiment_result, sentiment_scores, word_type_scores

      # Function to save learned actions to a file
      def learn_action(is_positive, phrase):
        category = "positive" if is_positive else "negative"
        state.update_learned_actions(category, phrase)
        state.save_learned_actions_to_file('learned_actions.json')


      def create_user_decide_popup(user_text):
          def close_popup():
              popup.destroy()
          def handle_positive_sentiment():
              learn_action(True, user_text)
              close_popup()

          def ai_decide_sentiment():
              sentiment_result = get_sentiment(user_text)[0]
              if sentiment_result != "negative":
                # Before creating sentiment buttons, close the current pop-up
                close_popup()
                create_sentiment_buttons(user_text)
              else:
                messagebox.showinfo(
                    "Sentiment Decision",
                    "The sentiment is negative and will not be saved.")
                # Ensuring we close the pop-up even when sentiment is negative
                close_popup()

            # Here we define the pop-up using top-level instead of creating a new Tk root
                popup = tk.Toplevel()
                popup.title("Your Input is Needed")

                tk.Label(popup, text="We need your help with the sentiment.").pack()
                tk.Button(popup,
                      text="This is Positive",
                      command=handle_positive_sentiment).pack()
                tk.Button(popup, text="You Decide", command=ai_decide_sentiment).pack()

                close_button = tk.Button(popup, text="Close", command=close_popup)
                close_button.pack()

                popup.grab_set()  # this will direct all events to the pop-up
                popup.focus_set()  # this will focus on the pop-up


      def check_learned_phrases(text):
        learned_phrases = state.learned_actions  # use the in-memory data

        for sentiment, phrases in learned_phrases.items():
          if text in phrases:
            return sentiment
        return None


      # Modify get_response function in the main.py file
      def get_response(text):
          try:
            sentiment_result, sentiment_scores, word_type_scores = analyze_text(text)
            learned_sentiment = check_learned_phrases(text)
            # Check for greetings and farewells first
            if any(greeting in text.lower() for greeting in state.greetings):  # Using state instance
              response = f"{random.choice(state.greetings).capitalize()}! How can I help you today?" 
              # Using state instance
            elif any(farewell in text.lower() for farewell in state.farewells):  # Using state instance
              response = f"{random.choice(state.farewells).capitalize()}! Have a great day!"
              # Using state instance
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
                create_user_decide_popup(text)
              else:
                if sentiment_result == "negative":
                  learn_action(False, text)
                elif sentiment_result == "positive":
                  learn_action(True, text)
                if sentiment_result != "neutral":
                  learn_action(sentiment_result == "positive", text)
                  response_results(sentiment_result, sentiment_scores, word_type_scores)
            return response
          except Exception as e:
            logging.error(f"An error occurred in get_response: {e}")
          return "I'm sorry, but an error occurred while generating a response."


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

        popup = tk.Tk()
        popup.title("Sentiment Undetermined")
        tk.Label(popup, text="Unable to determine sentiment.").pack()
        tk.Button(popup,
                  text="Sentiment is Positive",
                  command=handle_positive_sentiment).pack()
        tk.Button(popup, text="Sentiment is Negative", command=close_popup).pack()
        popup.mainloop()

        def handle_positive_sentiment():
          learn_action(True, user_text)
        popup.destroy()


      def on_submit():
        # REMOVE the unnecessary use of global root
        try:
          user_input = text_entry.get()  # No need to declare text_entry as global if it's not used outside this scope
          threading.Thread(target=lambda: get_response_and_save(user_input), daemon=True).start()
        except Exception as e:
          logging.error(f"An error occurred in on_submit: {e}")
          messagebox.showerror("Error", str(e))



      def get_response_and_save(user_input):
        response = get_response(user_input)  # get the response based on user input
        messagebox.showinfo("Response", response)
        # Replace the incorrect function call with the GlobalState method
        state.save_learned_actions_to_file('learned_actions.json')  # save any updated learned actions



      # TKinter popup creation
        def create_popup():
          global root  # We might not need this if root is not used elsewhere outside this scope
          root = tk.Tk()
          root.title("Text Input")
          global text_entry  # This does need to be global since it's accessed in on_submit
          text_entry = tk.Entry(root, width=50)
          text_entry.pack()
          submit_button = tk.Button(root, text="Submit", command=on_submit)
          submit_button.pack()
          root.mainloop()


          def on_program_exit():
            try:
              # ... existing code to save the state
               pass
            except Exception as e:
              logging.error(f"Failed to save all data on exit: {e}")
            finally:
              if 'root' in globals():
                root.destroy()  # Check if 'root' is defined before destroying it
              print("Program exiting...")# Main Execution Corrections

if __name__ == "__main__":
    state = GlobalState()
    try:
        # Assuming you have a method to load the state from a file
        state.load_words_from_file('words.json')
        state.load_learned_actions_from_file('learned_actions.json')
        create_popup()  # This initializes and starts the Tkinter GUI event loop
    except Exception as e:
        messagebox.showerror("Error", str(e))
    # root.protocol is set after initialization and within the Tkinter mainloop,
    # so it's unnecessary in this else block.
