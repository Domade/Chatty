import os
import random
import logging
import unittest

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


def convert_text_to_speech(text):
    speech_key = "421ccfbe89054d5eb5d259152b5d0e1b"
    speech_region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.AudioConfig(filename="output.wav")
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully.")
        main_dir = os.path.dirname(__file__)
        wav_file = os.path.join(main_dir, 'output.wav')
        
        with open(wav_file, 'wb') as f:
            f.write(result.audio_data)
            
        print("Speech output saved as {}".format(wav_file))
        
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Speech synthesis canceled: {}".format(result.cancellation_details.reason))
        
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(result.cancellation_details.error_details))
def main():
    text = input("Enter the text that you want to convert to speech: ")
    convert_text_to_speech(text)
    
    lst = random.sample(range(1, 21), 10)
    lst.sort()
    target = random.randint(1, 20)
if __name__ == "__main__":
    main()
    
    text = input("Enter the text that you want to convert to speech: ")
    while True:
        result = speech_synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized successfully.")
            main_dir = os.path.dirname(__file__)
            wav_file = os.path.join(main_dir, 'output.wav')
            
            with open(wav_file, 'wb') as f:
                f.write(result.audio_data)
                
            print("Speech output saved as {}".format(wav_file))
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            print("Speech synthesis canceled: {}".format(result.cancellation_details.reason))
            
            if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(result.cancellation_details.error_details))
                
        if text.lower() == 'quit':
            break
class TestBinarySearch(unittest.TestCase):
    def test_binary_search(self):
        self.assertEqual(binary_search([2, 4, 6, 8, 10], 6), 2)
        self.assertEqual(binary_search([2, 4, 6, 8, 10], 5), -1)
        self.assertEqual(binary_search([], 1), -1)
if __name__ == "__main__":
    unittest.main()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Starting the program")
try:
    pass  # Placeholder for the code that may raise an exception
except Exception as e:
    logging.error("An error occurred: {}".format(e))
logging.info("Ending the program")
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized successfully.")
    
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
def binary_search(lst, target):
    low = 0
    high = len(lst) - 1
    
    while low <= high:
        mid = (low + high) // 2
        
        if lst[mid] == target:
            return mid
        
        elif target < lst[mid]:
            high = mid - 1
            
        else:
            low = mid + 1
            
    return -1
lst = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
target = 14
result = binary_search(lst, target)
if result == -1:
    text = "The target value {} is not found in the list.".format(target)
else:
    text = "The target value {} is found at index {} in the list.".format(target, result)
print(text)