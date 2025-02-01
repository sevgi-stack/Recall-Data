import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import nltk

# Ensure you have the necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load the Excel file with the correct header row
file_path = "Movement and Communication final_May 29 2023_20.31.xlsx"
sheet_name = "Recall"

# Load the Excel file, specifying the correct header row
df = pd.read_excel(file_path, sheet_name=sheet_name, header=[0, 1])
print("DataFrame loaded successfully.")
print("DataFrame Head:")
print(df.head())

# Combine multi-level columns into single level by joining with a separator
df.columns = [' '.join(col).strip() for col in df.columns.values]
print("Columns after flattening multi-level headers:")
print(df.columns)

# Define a function to preprocess text
def preprocess_text(text):
    if isinstance(text, str):
        text = text.lower()  # Convert to lowercase
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        words = word_tokenize(text)  # Tokenize the text
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words]  # Remove stopwords
        return ' '.join(filtered_words)
    else:
        return ""


# Combine all recall columns into a single list of processed responses
recall_columns = [col for col in df.columns if 'recall' in col.lower()]
print("Identified recall columns:")
print(recall_columns)

processed_responses = []
for col in recall_columns:
    for response in df[col]:
        processed_text = preprocess_text(response)
        if processed_text:  # Only add non-empty responses
            processed_responses.append(processed_text)

if not processed_responses:
    print("No valid text data found in the specified columns.")
else:
    # Join all processed responses into a single text
    all_text = ' '.join(processed_responses)

    # Generate word frequencies using CountVectorizer
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([all_text])
    word_counts = dict(zip(vectorizer.get_feature_names_out(), X.toarray()[0]))

    # Convert the word counts to a DataFrame
    word_counts_df = pd.DataFrame(list(word_counts.items()), columns=['Word', 'Frequency'])

    # Save the word counts to a CSV file
    output_file = "M_C_Final_word_frequency_analysis.csv"
    word_counts_df.to_csv(output_file, index=False)
    print(f"\nWord frequency analysis saved to {output_file}")

    # Display the 10 most common words
    print("\n10 Most Common Words:")
    print(word_counts_df.nlargest(10, 'Frequency'))

    # Check if there are words to generate a word cloud
    if word_counts:
        # Generate a word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)

        # Display the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Recall Responses')
        plt.show()
    else:
        print("No words to display in the word cloud.")
