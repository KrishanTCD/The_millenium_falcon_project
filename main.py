from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd

# Load your data
df = pd.read_csv('reddit_immigration.csv')

# Assuming your comments are in a column named 'body'
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if not word.lower() in stop_words]
    return " ".join(filtered_text)

df['cleaned_body'] = df['body'].apply(clean_text)
df.to_csv('cleaned_reddit_immigration.csv', index=False)

import matplotlib.pyplot as plt
from collections import Counter

# Assuming 'cleaned_body' is your cleaned text
words = [word for line in df['cleaned_body'] for word in line.split()]
word_counts = Counter(words)

most_common_words = word_counts.most_common(10)
words, counts = zip(*most_common_words)

plt.bar(words, counts)
plt.xlabel('Words')
plt.ylabel('Counts')
plt.xticks(rotation='vertical')
plt.show()

from textblob import TextBlob

def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

df['sentiment'] = df['cleaned_body'].apply(get_sentiment)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=1000)
tfidf_matrix = vectorizer.fit_transform(df['cleaned_body'])

# Now, tfidf_matrix contains the TF-IDF scores

from gensim import corpora, models
import gensim

# Prepare a list of words for LDA analysis
text_data = [line.split() for line in df['cleaned_body']]

dictionary = corpora.Dictionary(text_data)
corpus = [dictionary.doc2bow(text) for text in text_data]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)
topics = ldamodel.print_topics(num_words=4)

for topic in topics:
    print(topic)

if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
