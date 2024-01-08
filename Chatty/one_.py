# Import the libraries
# Import the logging module
import logging
import os

# Import the unittest module
import unittest

  # Import the random module
import random  # Align the import statement at the global level


# Use the correct attribute name with the correct case
voice_profile = speechsdk.VoiceProfile(azure.cognitiveservices.speech, speechsdk.VoiceProfileType.Online)

# Set up the Azure Text to Speech service
speech_key = "your-key"
speech_region = "your-region"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
audio_config = speechsdk.AudioConfig(filename="output.wav")

# Create a SpeechSynthesizer object
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Convert text to speech
text = "Hello, this is Azure Text to Speech."
result = speech_synthesizer.speak_text_async(text).get()

try:  # Add a try block here
    # Import the module using the correct name
    import azure.cognitiveservices.speech as speechsdk


except ImportError as e:
    print("Error: {}".format(e))
    print("Please make sure you have installed the required libraries.")
    exit()
# Define a main function
def main():
    # Your main logic goes here
  # Get the text from the user input
  text = input("Enter the text that you want to convert to speech: ")


# Generate a random list of 10 numbers between 1 and 20
lst = random.sample(range(1, 21), 10)
# Sort the list
lst.sort()
# Generate a random target value between 1 and 20
target = random.randint(1, 20)


text = "Hello, world!"

    # Convert the text to speech
result = speech_synthesizer.speak_text_async(text).get()
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Print a message
        print("Speech synthesized successfully.")
        # Save the speech output as a wav file
        main_dir = os.path.dirname(__file__)
        wav_file = os.path.join(main_dir, 'output.wav')
        with open(wav_file, 'wb') as f:
            f.write(result.audio_data)
        print("Speech output saved as {}".format(wav_file))
elif result.reason == speechsdk.ResultReason.Canceled:
        # Print a message
        print("Speech synthesis canceled: {}".format(result.cancellation_details.reason))
        # Check the cancellation reason
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            # Print the error details
            print("Error details: {}".format(result.cancellation_details.error_details))
# Call the main function only when the script is executed directly
if __name__ == "__main__":
    main()

# Get the text from the user input
text = input("Enter the text that you want to convert to speech: ")


while True:
        # Convert the text to speech
        result = speech_synthesizer.speak_text_async(text).get()
        # Check the result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # Print a message
            print("Speech synthesized successfully.")
            # Save the speech output as a wav file
            main_dir = os.path.dirname(__file__)
            wav_file = os.path.join(main_dir, 'output.wav')
            with open(wav_file, 'wb') as f:
                f.write(result.audio_data)
            print("Speech output saved as {}".format(wav_file))
        elif result.reason == speechsdk.ResultReason.Canceled:
            # Print a message
            print("Speech synthesis canceled: {}".format(result.cancellation_details.reason))
            # Check the cancellation reason
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                # Print the error details
                print("Error details: {}".format(result.cancellation_details.error_details))
        # If the user types 'quit', break the loop
        if text.lower() == 'quit':
            break  # This 'break' statement is now within the while loop
  # Otherwise, convert the text to speech and save the output as a wav file
  # Your code for text to speech conversion goes here


# Define a test class that inherits from unittest.TestCase
class TestBinarySearch(unittest.TestCase):

    # Define a test method that starts with test_
    def test_binary_search(self):
        # Use self.assertEqual to check if the expected and actual outputs are equal
        self.assertEqual(binary_search([2, 4, 6, 8, 10], 6), 2)
        self.assertEqual(binary_search([2, 4, 6, 8, 10], 5), -1)
        self.assertEqual(binary_search([], 1), -1)

# Run the test suite
if __name__ == "__main__":
    unittest.main()

# Set the logging level and format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Use logging.info to record the start of the program
logging.info("Starting the program")

# Use logging.error to record any errors that occur
try:
  # Your code for text to speech conversion goes here
      pass  # Placeholder for the code that may raise an exception
except Exception as e:
      logging.error("An error occurred: {}".format(e))

# Use logging.info to record the end of the program
logging.info("Ending the program")


# Check the result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized successfully.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

def binary_search(lst, target):
    """Performs binary search on a sorted list and a target value.

    Args:
        lst (list): A sorted list of numbers.
        target (int): A target value to search for.

    Returns:
        int: The index of the target value in the list, or -1 if not found.
    """
    # Your code for binary search goes here

# Define a function that performs binary search on a sorted list and a target value
def binary_search(lst, target):
    # Initialize the low and high indices
    low = 0
    high = len(lst) - 1
    # Loop until the low and high indices meet
    while low <= high:
        # Calculate the middle index
        mid = (low + high) // 2
        # Check if the middle element is equal to the target
        if lst[mid] == target:
            # Return the index of the element
            return mid
        # If the target is smaller than the middle element
        elif target < lst[mid]:
            # Update the high index to the left of the middle index
            high = mid - 1
        # If the target is larger than the middle element
        else:
            # Update the low index to the right of the middle index
            low = mid + 1
    # If the target is not found, return -1
    return -1

# Define an example list and target value
lst = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
target = 14

# Call the binary search function
result = binary_search(lst, target)

# Convert the result into a text representation
if result == -1:
    text = "The target value {} is not found in the list.".format(target)
else:
    text = "The target value {} is found at index {} in the list.".format(target, result)

# Print the text
print(text)
