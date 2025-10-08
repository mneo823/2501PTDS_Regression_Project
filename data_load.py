import re
import pandas as pd

def clean_column_name(column):
    # Replace any sequence of non-alphabetic characters with a single underscore
    column = re.sub(r'[^a-zA-Z]+', '_', column)
    # Remove leading/trailing underscores and convert to lowercase
    return column.strip('_').lower()

def clean_dataframe_columns(df):
    # Create a copy of the dataframe to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Step 1: Clean all column names
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Step 2: Drop 'area' column
    if 'area' in df.columns:
        df = df.drop(columns=['area'])
        print("Dropped 'area' column successfully!")

    # Step 3: Handle missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print("\nMissing values found in the following columns:")
        print(missing_values[missing_values > 0])
        
        # Fill numeric columns with their median (more robust to outliers than mean)
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                print(f"Filled {df[col].isnull().sum()} missing values in '{col}' with median: {median_val:.2f}")
        
        # For any remaining non-numeric columns, fill with mode
        remaining_cols = df.columns[df.isnull().any()].tolist()
        for col in remaining_cols:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            print(f"Filled missing values in '{col}' with mode: {mode_val}")

    # Step 4: Move 'total_emission' to the first position
    if 'total_emission' in df.columns:
        cols = df.columns.tolist()
        cols.remove('total_emission')
        df = df[['total_emission'] + cols]
        print("\nDataframe Columns cleaned and Reordered successfully!")

    return df