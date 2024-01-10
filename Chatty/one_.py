#pip install spacy
#python -m spacy download en_core_web_sm

      # Updated file: main.py

      # Import necessary libraries
      import spacy
      import sys
      import random
      import json
      import logging

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

      # Function to process and respond to input text
      def get_response(text):
          # Check for greetings, farewells, etc.
          # ...

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
              # ...
