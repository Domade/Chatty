# Function to categorize verbs
def categorize_verb(verb):
    action_verbs = ['runs', 'jumps', 'drives', 'sits']
    linking_verbs = ['sleeps']

    if verb in action_verbs:
        return ("action", 1)
    if verb in linking_verbs:
        return ("linking", 3)
    return None

# Function to categorize nouns
def categorize_noun(noun):
    common_nouns = ['dog', 'cat', 'mouse']
    thing_nouns = ['house', 'car']

    if noun in common_nouns:
        return ("common", 4)
    if noun in thing_nouns:
        return ("thing", 3)
    return None

# Function to categorize descriptors
def categorize_descriptor(descriptor):
    # Example: each descriptor receives a random subcategory
    # In your actual implementation, you should categorize them correctly
    descriptor_categories = {
        'proper': 1,
        'describing': 2,
        'quantitative': 3,
        'numerical': 4,
        'demonstrative': 5,
        'distributive': 6,
        'interrogative': 7,
        'possessive': 8
    }
    
    # For the purpose of this example, let's assign 'quick' to 'describing', etc.
    # In practice, you would define which descriptors belong to which subcategory.
    assignment = {'quick': 'describing', 'lazy': 'describing', 'sleepy': 'describing', 'happy': 'quantitative', 'sad': 'quantitative'}

    if descriptor in assignment:
        return (assignment[descriptor], descriptor_categories[assignment[descriptor]])
    return None

# Existing arrays
nouns = ['dog', 'cat', 'mouse', 'house', 'car']
verbs = ['runs', 'jumps', 'sleeps', 'drives', 'sits']
descriptors = ['quick', 'lazy', 'sleepy', 'happy', 'sad']
# ... Remaining parts of your program

while True:
    text = input("Enter the text that you want to check: ")
    if text.lower() == 'quit':
        sys.exit()  # This will terminate the program immediately
    words = text.split()  # Split the input text into individual words
    for word in words:
        lower_word = word.lower()
        
        # Check if it's a verb and get its category if so
        verb_cat = categorize_verb(lower_word)
        if verb_cat:
            cheat = True
            print(f"Verb found: {verb_cat[0]}, represented by number {verb_cat[1]}")
            break

        # Check if it's a noun and get its category if so
        noun_cat = categorize_noun(lower_word)
        if noun_cat:
            cheat = True
            print(f"Noun found: {noun_cat[0]}, represented by number {noun_cat[1]}")
            break

        # Check if it's a descriptor and get its category if so
        descriptor_cat = categorize_descriptor(lower_word)
        if descriptor_cat:
            cheat = True
            print(f"Descriptor found: {descriptor_cat[0]}, represented by number {descriptor_cat[1]}")
            break
        
        # Assuming binary_search is defined as previously and checks other word types

    if not cheat:
        print("What do you mean?")
    
    cheat = False  # Reset cheat for the next loop iteration
    # Continue with the rest of your program...
    # ...
