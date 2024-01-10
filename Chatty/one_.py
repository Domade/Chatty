def binary_search(lst, target):
    low = 0
    high = len(lst) - 1

    while low <= high:
        mid = (low + high) // 2
        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


while True:
    text = input("Enter the text that you want to convert to speech: ")
    if text.lower() == 'quit':
        break
    
    # rest of the code


try:
    pass  # Placeholder for the code that may raise an exception
except Exception as e:
    logging.exception("An error occurred")
