import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the dataset
file_path = "Raw_Response_Timestamps_transformed_data.xlsx"  # Input file
output_path = "Raw_Response_Timestamps_analysed_data.xlsx"   # Output file
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Display basic information about the dataset
print("Dataset Information:")
df.info()
print("\nFirst few rows of the dataset:")
print(df.head())

# Select only numerical columns for statistical analysis
numerical_cols = df.select_dtypes(include=[np.number]).columns

# Compute basic statistics
summary_stats = df[numerical_cols].describe()

# Z-Score Analysis to find significant outliers
z_scores = np.abs(stats.zscore(df[numerical_cols], nan_policy='omit'))
outliers = (z_scores > 3).sum(axis=0)  # Count how many values are outliers per column
outlier_df = pd.DataFrame({'Column': numerical_cols, 'Outlier Count': outliers})

# Correlation Matrix
correlation_matrix = df[numerical_cols].corr()

# ANOVA test to check differences in intensity metrics across different visibility levels
anova_results = {}
if "visibility" in df.columns:
    categories = df["visibility"].dropna().unique()
    if len(categories) > 1:
        for col in numerical_cols:
            groups = [df[df["visibility"] == cat][col].dropna() for cat in categories]
            if all(len(group) > 1 for group in groups):  # Ensure each group has data
                f_stat, p_value = stats.f_oneway(*groups)
                anova_results[col] = {"F-Statistic": f_stat, "P-Value": p_value}

anova_df = pd.DataFrame(anova_results).T

# T-Test for intensity between high and low visibility groups
t_test_results = {}
if "visibility" in df.columns and "intensity_general" in df.columns:
    high_visibility = df[df["visibility"] == "high"]["intensity_general"].dropna()
    low_visibility = df[df["visibility"] == "low"]["intensity_general"].dropna()
    if not high_visibility.empty and not low_visibility.empty:
        t_stat, p_value = stats.ttest_ind(high_visibility, low_visibility)
        t_test_results = {
            "T-Statistic": t_stat,
            "P-Value": p_value,
            "Significant": p_value < 0.05
        }

# Save results to an Excel file
with pd.ExcelWriter(output_path) as writer:
    summary_stats.to_excel(writer, sheet_name='Summary_Statistics')
    outlier_df.to_excel(writer, sheet_name='Outliers')
    correlation_matrix.to_excel(writer, sheet_name='Correlation_Matrix')
    anova_df.to_excel(writer, sheet_name='ANOVA_Results')
    pd.DataFrame([t_test_results]).to_excel(writer, sheet_name='T_Test_Results')

print(f"\nAnalysis completed. Results saved to {output_path}")
