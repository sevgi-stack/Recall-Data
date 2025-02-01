import pandas as pd

# Load the Excel file and the specific worksheet
file_path = 'Movement and Communication final_May 29 2023_20.31.xlsx'
sheet_name = 'Recall'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Display initial information about the DataFrame
print("Initial DataFrame Info:")
print(df.info())
print("\nInitial DataFrame Head:")
print(df.head())

# Data Cleaning: Handle missing values
# Option 1: Drop rows where all elements are missing
df_cleaned = df.dropna(how='all')

# Option 2: Fill missing values with a placeholder (e.g., 'Unknown' for categorical data)
df_filled = df_cleaned.fillna('Unknown')

# Data Structuring: Organize data into categories

# Demographic Information
demographic_columns = ['age', 'gender']
df_demographics = df_filled[demographic_columns]

# Recall Responses
recall_columns = [col for col in df_filled.columns if 'recall' in col]
df_recall = df_filled[recall_columns]

# Video Call Experiences
video_call_columns = [col for col in df_filled.columns if 'videocall' in col or 'frequency' in col or 'platform' in col]
df_video_call = df_filled[video_call_columns]

# Display cleaned and structured data
print("\nCleaned DataFrame Info:")
print(df_filled.info())
print("\nDemographic Information:")
print(df_demographics.head())
print("\nRecall Responses:")
print(df_recall.head())
print("\nVideo Call Experiences:")
print(df_video_call.head())

# Save cleaned data to new Excel files (optional)
df_filled.to_excel('M_C_Final_Cleaned_Data.xlsx', index=False)
df_demographics.to_excel('M_C_Final_Demographic_Information.xlsx', index=False)
df_recall.to_excel('M_C_Final_Recall_Responses.xlsx', index=False)
df_video_call.to_excel('M_C_Final_Video_Call_Experiences.xlsx', index=False)
