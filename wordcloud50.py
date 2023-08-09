from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import ast

# Load the data
##mac load 
data_path = r'/Users/evan/Desktop/data_with_NLP.csv'
#data_path = r'C:\Users\Evan Anderson\Desktop\data_with_NLP.csv'
df = pd.read_csv(data_path)


# Extract comments and sentiments
comments = df['new_comment']
sentiments = df['nlp_sid']

# Combine all comments into a single text
all_text = ' '.join(comments)

# Tokenize and count word occurrences while removing stop words
vectorizer = CountVectorizer(stop_words='english')
word_counts = vectorizer.fit_transform([all_text])
words = vectorizer.get_feature_names_out()
word_counts = word_counts.toarray()[0]

# Create a dictionary of word frequencies and sentiment scores
word_data = {word: {'frequency': count, 'sentiments': []} for word, count in zip(words, word_counts)}

# Collect sentiment scores for each word
for i, row in df.iterrows():
    for word in row['new_comment'].split():
        if word in word_data:
            sentiment = ast.literal_eval(row['nlp_sid'])  # Convert string to dictionary
            word_data[word]['sentiments'].append(sentiment)

# Calculate average sentiment scores for each word
for word, data in word_data.items():
    if data['sentiments']:
        average_sentiment = np.mean([sentiment['compound'] for sentiment in data['sentiments']])
        data['average_sentiment'] = average_sentiment
    else:
        data['average_sentiment'] = 0

# Determine colors based on average sentiment
word_colors = {word: 'blue' if data['average_sentiment'] > 0 else 'red' for word, data in word_data.items()}

# Create a WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white', color_func=lambda *args, **kwargs: word_colors.get(args[0], 'black')).generate_from_frequencies({word: data['frequency'] for word, data in word_data.items()})

# Create the WordCloud plot with colors
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
