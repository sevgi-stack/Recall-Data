import pandas as pd
import re

# Load the Excel file
file_path = 'Raw_Response_Timestamps(Movementstudy).xlsx'  # Replace with your actual file path
sheet_name = 'Movement_timestamps'  # Replace with your actual sheet name if different
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Display the first few rows of the dataframe
print("Original Data:")
print(df.head())

# Function to convert a time string 'MM:SS' or 'H:MM:SS' to total seconds
def time_to_seconds(time_str):
    try:
        parts = list(map(int, time_str.split(':')))
        if len(parts) == 2:  # MM:SS
            minutes, seconds = parts
            hours = 0
        elif len(parts) == 3:  # H:MM:SS
            hours, minutes, seconds = parts
        else:
            raise ValueError
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        print(f"Unexpected time format: {time_str}")
        return 0

# Function to process a single cell containing multiple time intervals
def process_time_intervals(cell):
    total_seconds = 0
    interval_count = 0
    # Extract all time intervals using regular expressions
    intervals = re.findall(r'\d{1,2}:\d{2}-\d{1,2}:\d{2}', str(cell))
    for interval in intervals:
        start_time, end_time = interval.split('-')
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)
        # Calculate the duration of the interval
        interval_seconds = end_seconds - start_seconds
        total_seconds += interval_seconds
        interval_count += 1
    return total_seconds, interval_count

# List of columns to process
columns_to_process = ['general_topic', 'self_positive', 'self_negative', 'other_positive', 'other_negative']

# Apply the processing function to each specified column
for column in columns_to_process:
    if column in df.columns:
        df[[f'{column}_total_seconds', f'{column}_interval_count']] = df[column].apply(
            lambda cell: pd.Series(process_time_intervals(cell))
        )
        # Calculate the average duration per interval
        df[f'{column}_average_seconds'] = df.apply(
            lambda row: row[f'{column}_total_seconds'] / row[f'{column}_interval_count']
            if row[f'{column}_interval_count'] > 0 else 0,
            axis=1
        )
    else:
        print(f"Column '{column}' not found in the DataFrame.")

# Display the transformed data
print("\nTransformed Data:")
print(df.head())

# Save the transformed data to a new Excel file
output_file_path = 'Raw_Response_Timestamps_transformed_data.xlsx'  # Specify your desired output file path
df.to_excel(output_file_path, index=False)
