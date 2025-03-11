import pandas as pd
import re
from difflib import SequenceMatcher
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def clean_column_names(df):
    """
    Standardize column names in a DataFrame.

    This function takes a pandas DataFrame and standardizes its column names by:
    - Stripping leading and trailing whitespace
    - Converting all characters to lowercase
    - Replacing spaces with underscores
    - Replacing slashes with underscores

    Parameters:
        df (pandas.DataFrame): The DataFrame whose column names need to be standardized.

    Returns:
        pandas.DataFrame: The DataFrame with standardized column names.
    """
    
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/', '_')
    return df


def adjust_column_names_for_download(df):
    """
    Adjusts the column names of a DataFrame for download.

    This function modifies the column names of the given DataFrame by:
    1. Stripping any leading or trailing whitespace.
    2. Replacing underscores with spaces.
    3. Converting the column names to title case.

    Parameters:
        df (pandas.DataFrame): The DataFrame whose column names need to be adjusted.

    Returns:
        pandas.DataFrame: The DataFrame with adjusted column names.
    """
    df.columns = df.columns.str.strip().str.replace('_', ' ').str.title()
    return df

def calculate_data_metrics(df):
    """
    Calculate key metrics for data quality checks.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze.
    
    Returns:
        dict: Metrics including total rows, unique webmails, duplicate webmails,
              and members not using webmail.
    """
    metrics = {
        'total_rows': len(df),
        'unique_webmails': df['pup_webmail'].nunique() if 'pup_webmail' in df.columns else 0,
        'duplicate_webmails': df.duplicated(subset=['pup_webmail']).sum() if 'pup_webmail' in df.columns else 0,
        'non_webmail_members': df['pup_webmail'].isna().sum() if 'pup_webmail' in df.columns else 0
    }
    return metrics

def analyze_text_case(df, columns):
    """
    Analyze text case (uppercase, lowercase, title case) for specified columns.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze.
        columns (list): List of column names to analyze.
    
    Returns:
        pd.DataFrame: Dataframe with counts of uppercase, lowercase, and title case for each column.
    """
    case_analysis = {}
    for col in columns:
        if col in df.columns:
            # Handle NaN values by replacing with empty strings
            col_values = df[col].fillna('')
            
            # Count uppercase, lowercase, and title case
            uppercase = col_values.str.isupper().sum()
            lowercase = col_values.str.islower().sum()
            titlecase = col_values.str.istitle().sum()
            
            case_analysis[col] = {
                'Uppercase': uppercase,
                'Lowercase': lowercase,
                'Title Case': titlecase
            }
    return pd.DataFrame(case_analysis)

def find_similar_strings_with_rows(df, column, threshold=0.8):
    """
    Find similar strings within a specified column of a DataFrame and return the pairs of similar strings along with the rows containing them.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to search for similar strings.
        column (str): The column name in the DataFrame to search for similar strings.
        threshold (float): The similarity threshold (default is 0.8). Strings with a similarity ratio above this threshold are considered similar.
    
    Returns:
        tuple: A tuple containing two DataFrames:
            - pairs_df (pd.DataFrame): A DataFrame containing pairs of similar strings and their similarity scores.
            - matching_rows (pd.DataFrame): A DataFrame containing the rows from the original DataFrame that match either value1 or value2 from pairs_df.
    """

    if column not in df.columns or df[column].dtype not in ['object', 'category']:
        return pd.DataFrame(), pd.DataFrame()

    unique_values = df[column].dropna().unique()
    similar_pairs = []

    def normalize_string(s):
        if not isinstance(s, str):
            return ""
        s = s.lower()
        s = " ".join(s.split())
        s = re.sub(r'[^\w\s]', '', s)
        return s

    def string_similarity(s1, s2):
        s1_norm = normalize_string(s1)
        s2_norm = normalize_string(s2)
        if not s1_norm or not s2_norm:
            return 0.0
        return SequenceMatcher(None, s1_norm, s2_norm).ratio()

    for i, val1 in enumerate(unique_values):
        for val2 in unique_values[i + 1:]:
            similarity = string_similarity(val1, val2)
            if similarity >= threshold:
                similar_pairs.append({
                    'value1': val1,
                    'value2': val2,
                    'similarity': round(similarity, 3)
                })

    pairs_df = pd.DataFrame(similar_pairs)

    if pairs_df.empty:
      return pairs_df, pd.DataFrame()

    # Find rows that match either value1 or value2
    matching_rows = df[df[column].isin(pairs_df['value1'].tolist() + pairs_df['value2'].tolist())]

    return pairs_df, matching_rows

