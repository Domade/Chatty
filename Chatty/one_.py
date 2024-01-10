# Existing binary search function
# ...
# Arrays for descriptive parts of speech
nouns = ['dog', 'cat', 'mouse', 'house', 'car']
verbs = ['runs', 'jumps', 'sleeps', 'drives', 'sits']
descriptors = ['quick', 'lazy', 'sleepy', 'happy', 'sad']
conjunctions = ['and', 'or', 'but', 'because', 'if', 'while', 'although']
cheat = False  # Variable to track if a descriptor is found
while True:
    text = input("Enter the text that you want to check: ")
    if text.lower() == 'quit':
        sys.exit()  # This will terminate the program immediately
    words = text.split()  # Split the input text into individual words
    # Check for descriptors, nouns, verbs, and conjunctions in the input text
    for word in words:
        if binary_search(descriptors, word) != -1 or binary_search(nouns, word) != -1 or \
           binary_search(verbs, word) != -1 or binary_search(conjunctions, word) != -1:
            cheat = True
            print("Descriptor, noun, verb, or conjunction found.")
            break  # No need to check further if a descriptive part of speech is found
    if not cheat:
        print("What do you mean?")
    # Reset cheat for the next loop iteration
    cheat = False
    # Continue with the rest of your program...
    # ...