  # Simplified sentiment analysis function
  def get_sentiment(text):
    positive_words = ['good', 'great', 'awesome', 'happy', 'love']
    negative_words = ['bad', 'sad', 'terrible', 'hate', 'unhappy']
    score = 0
    # Assign a score of +1 for each positive word, and -1 for each negative word
    for word in text.lower().split():
      if word in positive_words:
        score += 1
      elif word in negative_words:
        score -= 1
    # Determine sentiment based on the final score
    if score > 0:
      return "positive"
    elif score < 0:
      return "negative"
    else:
      return "neutral"
