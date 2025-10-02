import re

def clean_column_name(column):
    # Replace any sequence of non-alphabetic characters with a single underscore
    column = re.sub(r'[^a-zA-Z]+', '_', column)
    # Remove leading/trailing underscores and convert to lowercase
    return column.strip('_').lower()

def clean_dataframe_columns(df):
    # Step 1: Clean all column names
    df.columns = [clean_column_name(col) for col in df.columns]

    # Step 2: Move 'total_emission' to the first position if it exists
    if 'total_emission' in df.columns:
        cols = df.columns.tolist()
        cols.remove('total_emission')
        df = df[['total_emission'] + cols]
        print("Reordered columns successfully!")

    return df