S1: create conda environment conda create --name your_env_name
S2: Activate this by conda activate your_env_name
S3: Run: python env_setup.py install
S4:

2.2. Cleaning Script
Your cleaning script will:

Remove stopwords using NLTK.
Remove low-frequency words to reduce the dimensionality of your dataset.
Detect and remove comments in languages other than English using langdetect.
Remove emojis using the emoji library.

The analysis will involve several steps:

Word Distribution: Use matplotlib to visualize the frequency distribution of words.
Sentiment Analysis: textblob can be used to determine the sentiment of comments.
TF-IDF and Term Frequency: Utilize scikit-learn for TF-IDF and term frequency vector models.
LDA Topic Modeling: Use gensim for LDA modeling to identify topics within the data related to immigration in the USA.
