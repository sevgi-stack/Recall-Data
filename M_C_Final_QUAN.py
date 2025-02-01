import pandas as pd

# Load the Excel file and select the 'Recall' worksheet
file_path = "Movement and Communication final_May 29 2023_20.31.xlsx"
sheet_name = "Recall"
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Data Cleaning: Remove columns with all missing values
df.dropna(axis=1, how='all', inplace=True)

# Data Cleaning: Fill missing values
# Separate numeric and non-numeric columns
numeric_cols = df.select_dtypes(include='number').columns
non_numeric_cols = df.select_dtypes(exclude='number').columns

# Fill missing values in numeric columns with the median
df[numeric_cols] = df[numeric_cols].apply(lambda col: col.fillna(col.median()))

# Fill missing values in non-numeric columns with 'Unknown'
df[non_numeric_cols] = df[non_numeric_cols].fillna('Unknown')

# Descriptive Statistics: Calculate mean, median, mode, and standard deviation for numeric columns
descriptive_stats = df[numeric_cols].agg(['mean', 'median', 'std']).transpose()
mode_stats = df[numeric_cols].mode().transpose()
mode_stats.columns = ['mode']
descriptive_stats = descriptive_stats.join(mode_stats)

# Frequency Analysis: Determine the frequency of each response for non-numeric columns
frequency_analysis = {col: df[col].value_counts() for col in non_numeric_cols}

# Cross-Tabulation: Examine relationships between different variables
# Example: Cross-tabulation between 'gender' and 'platform'
if 'gender' in df.columns and 'platform' in df.columns:
    cross_tab = pd.crosstab(df['gender'], df['platform'])
else:
    cross_tab = pd.DataFrame()

# Save results to an Excel file
output_file = "M_C_Final_Quantitative_Analysis_Results.xlsx"
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    descriptive_stats.to_excel(writer, sheet_name='Descriptive_Stats')
    cross_tab.to_excel(writer, sheet_name='Cross_Tab_Gender_Platform')
    # Save frequency analysis results
    for col, freq_df in frequency_analysis.items():
        # Ensure sheet name does not exceed 31 characters
        sheet_name = f'Freq_{col}'[:31]
        freq_df.to_frame().to_excel(writer, sheet_name=sheet_name)

print(f"Analysis complete. Results saved to {output_file}.")
