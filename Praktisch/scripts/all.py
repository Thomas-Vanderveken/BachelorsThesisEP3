import pandas as pd
import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to clean and preprocess the text
def clean_text(text):
    # Remove unwanted characters and excessive whitespace
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'\s+', ' ', text)   # Replace multiple spaces with single space
    return text.strip()

# Function to extract structured data from cleaned text
def extract_table_data(text):
    # Define patterns for extracting table columns
    patterns = {
        'Issuer': r'^(.*?)(?= \d{3,4})',  # Pattern for issuer names
        'CUSIP': r'\b[A-Z0-9]{6,9}\b',  # CUSIPs, allowing letters and numbers
        'Value': r'\d+(?:,\d{3})*(?:\.\d+)?',  # Numeric values
        'Shares': r'\d+(?:,\d{3})*',  # Number of shares
    }
    
    # Initialize results
    extracted_data = []
    
    # Clean the text
    cleaned_text = clean_text(text)
    
    # Tokenize and process text
    doc = nlp(cleaned_text)
    
    # Extracting based on regex patterns
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, cleaned_text)
        for match in matches:
            extracted_data.append({pattern_name: match})
    
    return extracted_data

# Function to process the CSV file and extract table data
def process_csv_file(csv_file):
    df = pd.read_csv(csv_file)
    
    for index, row in df.iterrows():
        info_table_text = row['Information Table']
        
        if pd.notna(info_table_text):
            data = extract_table_data(info_table_text)
            print(f"File: {row['Filename']}")
            print("Extracted Data:")
            for entry in data:
                print(entry)
            print("\n")

# Example usage
csv_files = ['./13f_filings_summary.csv']  # Replace with your CSV file names
for file in csv_files:
    process_csv_file(file)
