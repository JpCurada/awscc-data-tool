import pandas as pd

def clean_column_names(df):
  df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/', '_')
  return df

def standardize_birthday_col(df):
  df.birthdate = pd.to_datetime(df.birthdate, errors='coerce').dt.strftime('%Y-%m-%d')
  return df

def standardize_text_data(df):
  for col in df.select_dtypes('object').columns:
    if col in ['program', 'campus', 'year_level']:
      df[col] = df[col].str.strip().str.upper()
    if col.contains('name'):
      df[col] = df[col].str.strip().str.title()
    if col.contains('mail'):
      df[col] = df[col].str.strip().str.lower()
  return df

def detect_duplicates_by_cols(df, column_list):
  return df[(df.duplicated(subset=column_list, keep=False)) & ~df[column_list].isna()]

def detect_missing_val_by_cols(df, column_list):
  return df[df[column_list].isna().any(axis=1)]


