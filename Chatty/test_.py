import random
import string

def generate_password(length):
  # create a list of characters to choose from
  chars = string.ascii_letters + string.digits + string.punctuation
  # create an empty string to store the password
  password = ""
  # loop through the length of the password
  for i in range(length):
    # choose a random character from the list
    char = random.choice(chars)
    # append the character to the password
    password += char
  # return the password
  return password

# test the function
print(generate_password(10))
