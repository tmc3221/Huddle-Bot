import pandas as pd
import zipfile
import os

def load_csv_from_file(csv_path):
    # Load the mock data from a single CSV
    return pd.read_csv(csv_path)

'''
def load_csvs_from_zip(zip_path):
    # Create a directory to extract files
    extract_dir = 'extracted_files'
    os.makedirs(extract_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Unzip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Store data frames
    dfs = []

    # Loop through extracted files
    for file_name in os.listdir(extract_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(extract_dir, file_name)
            print(f"Loading {file_name}...")
            df = pd.read_csv(file_path)
            dfs.append(df)  # Append data frame
    
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df
'''