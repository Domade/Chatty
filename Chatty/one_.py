# Arrays for descriptive parts of speech
nouns = ['dog', 'cat', 'mouse', 'house', 'car']
verbs = ['runs', 'jumps', 'sleeps', 'drives', 'sits']
descriptors = ['quick', 'lazy', 'sleepy', 'happy', 'sad']
conjunctions = ['and', 'or', 'but', 'because', 'if', 'while', 'although']

# Identifier dictionaries
noun_identifiers = {word: list(range(1, 5)) for word in nouns} # 4 numbers for nouns
verb_identifiers = {word: list(range(1, 4)) for word in verbs} # 3 numbers for verbs
descriptor_identifiers = {word: list(range(1, 9)) for word in descriptors} # 8 numbers for descriptors

cheat = False  # Variable to track if a descriptor is found
while True:
    text = input("Enter the text that you want to check: ")
    if text.lower() == 'quit':
        sys.exit()  # This will terminate the program immediately
    words = text.split()  # Split the input text into individual words
    # Check for descriptors, nouns, verbs, and conjunctions in the input text
    for word in words:
        identified = False
        lower_word = word.lower()
        if lower_word in noun_identifiers:
            cheat = True
            identified = True
            print(f"Noun found: {word}, represented by numbers {noun_identifiers[lower_word]}")
        elif lower_word in verb_identifiers:
            cheat = True
            identified = True
            print(f"Verb found: {word}, represented by numbers {verb_identifiers[lower_word]}")
        elif lower_word in descriptor_identifiers:
            cheat = True
            identified = True
            print(f"Descriptor found: {word}, represented by numbers {descriptor_identifiers[lower_word]}")
        if identified:
            break  # No need to check further if the word has been identified

    if not cheat:
        print("What do you mean?")
    
    # Reset cheat for the next loop iteration
    cheat = False
    # Continue with the rest of your program...
    # ...
