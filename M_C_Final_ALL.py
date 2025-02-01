import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the dataset
file_path = 'Movement and Communication final_May 29 2023_20.31.csv'  # Replace with your actual file path
df = pd.read_csv(file_path)

# Display basic information about the dataset
print("Dataset Information:")
df.info()
print("\nFirst few rows of the dataset:")
print(df.head())

# Identify numerical columns
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Convert columns that should be numeric
# Assuming 'age' and 'intensity_general' should be numeric
for col in ['age', 'intensity_general']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Update numerical columns list after conversion
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Handle missing values
# For numerical columns, fill missing values with the median
df[numerical_cols] = df[numerical_cols].apply(lambda x: x.fillna(x.median()), axis=0)

# For categorical columns, fill missing values with the mode
categorical_cols = df.select_dtypes(include=[object]).columns
df[categorical_cols] = df[categorical_cols].apply(lambda x: x.fillna(x.mode()[0]), axis=0)

# Descriptive Statistics
print("\nDescriptive Statistics:")
print(df.describe(include='all'))

# Data Visualization
# Histogram for numerical columns
if numerical_cols:
    df[numerical_cols].hist(bins=15, figsize=(15, 6), layout=(2, 3))
    plt.suptitle('Histograms of Numerical Columns')
    plt.show()
else:
    print("No numerical columns available for plotting histograms.")

# Bar plot for categorical columns
for col in categorical_cols:
    plt.figure(figsize=(10, 4))
    sns.countplot(data=df, x=col)
    plt.title(f'Count Plot of {col}')
    plt.xticks(rotation=45)
    plt.show()

# Box plot to identify outliers in numerical columns
if numerical_cols:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[numerical_cols])
    plt.title('Box Plot of Numerical Columns')
    plt.xticks(rotation=45)
    plt.show()
else:
    print("No numerical columns available for box plots.")

# Qualitative Data Analysis
# Assuming 'general_topic' is a textual column containing qualitative data
if 'general_topic' in df.columns:
    from sklearn.feature_extraction.text import CountVectorizer
    from wordcloud import WordCloud

    text_data = df['general_topic'].dropna()
    vectorizer = CountVectorizer(stop_words='english')
    term_matrix = vectorizer.fit_transform(text_data)
    term_freq = np.asarray(term_matrix.sum(axis=0)).flatten()
    terms = vectorizer.get_feature_names_out()
    term_freq_df = pd.DataFrame({'term': terms, 'frequency': term_freq})
    term_freq_df = term_freq_df.sort_values(by='frequency', ascending=False)

    # Display the most common terms
    print("\nMost Common Terms in 'general_topic':")
    print(term_freq_df.head(10))

    # Generate a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(text_data))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of General Topics')
    plt.show()

# Statistical Analysis
# Example: T-test to compare 'intensity_general' between 'high' and 'low' visibility groups
if 'visibility' in df.columns and 'intensity_general' in df.columns:
    high_visibility = df[df['visibility'] == 'high']['intensity_general']
    low_visibility = df[df['visibility'] == 'low']['intensity_general']
    t_stat, p_value = stats.ttest_ind(high_visibility.dropna(), low_visibility.dropna())
    print(f"\nT-test between 'high' and 'low' visibility groups for 'intensity_general':")
    print(f"T-statistic: {t_stat}, P-value: {p_value}")

    if p_value < 0.05:
        print("Result: Statistically significant difference.")
    else:
        print("Result: No statistically significant difference.")
