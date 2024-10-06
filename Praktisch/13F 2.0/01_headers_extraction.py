import os
import re
import pandas as pd
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# Ensure you have the necessary NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Define a function to preprocess and clean text
def preprocess_text(text):
    # Tokenize text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    # Convert to lowercase and remove punctuation
    words = [word.lower() for word in words if word.isalnum()]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    return sentences, words

# Extract information using text mining
def extract_info(text):
    # Regular expressions to capture various fields
    fields = {
        'Type': re.search(r"\<TYPE\>(.*)", text),
        'Filename': re.search(r"\<FILENAME\>(.*)", text),
        'Description': re.search(r"\<DESCRIPTION\>(.*)", text),
        'Report Date': re.search(r"Report for the Calendar Year or Quarter Ended:\s*(.*)", text),
        'Company Name': re.search(r"Institutional Investment Manager Filing this Report:\s*Name:\s*(.*)", text),
        'Addres1': re.search(r"Address:\s*(.*)", text),
        'Addres2': re.search(r'Address:[^\n]*\n\s*([^\n]+)', text),
        'File Number': re.search(r"13F File Number:\s*(.*)", text),
        'Person Name': re.search(r"Person Signing this Report on Behalf of Reporting Manager:\s*Name:\s*(.*)", text, re.IGNORECASE),
        'Title': re.search(r"Title:\s*(.*)", text),
        'Phone': re.search(r"Phone:\s*(.*)", text),
        'Signature': re.search(r"Signature\s*,\s*Place,\s*and\s*Date\s*of\s*Signing:\s*(.*)", text),
        'Report Type': re.search( r'\[\s*x\s*\]\s+(13F HOLDINGS REPORT|13F NOTICE|13F COMBINATION REPORT)', text, re.IGNORECASE),
        # 'Report Summary - num managers': re.search(r'Number of Other Included Managers:\s*(\d+)\s*', text),
        # 'Report Summary - IT total entry': re.search( r'Form 13F Information Table Entry Total:\s*(\d+)\s*', text),
        # 'Report Summary - IT total value': re.search(r'Form 13F Information Table Value Total:\s*\$([\d,]+)', text),
        # 'List of other Included Managers': re.search(r'No\.\s+(\d+)\s*[\r\n]+Form 13F File Number:\s*([\d\-]+)\s*[\r\n]+Name:\s*(.*?)\s*(?=<PAGE>|No\.|\Z)', text),
    }
    
    # Extract fields with default 'N/A' if not found
    extracted = {key: (match.group(1).strip() if match else 'N/A') for key, match in fields.items()}
    report_summary = {
        'Number of Other Included Managers': re.search(r'Number\s*of\s*Other\s*Included\s*Managers\s*:\s*(\d+)\s*', text, re.IGNORECASE),
        'Information Table Entry Total': re.search(r'Form\s*13F\s*Information\s*Table\s*Entry\s*Total\s*:\s*(\d+)\s*', text, re.IGNORECASE),
        'Information Table Value Total': re.search(r'Form\s*13F\s*Information\s*Table\s*Value\s*Total\s*:\s*\$([\d,]+)', text, re.IGNORECASE)
    }
    
    # Extract summary fields with default 'N/A' if not found and merge them
    extracted['Report Summary'] = {
        report_summary['Number of Other Included Managers'].group(1).strip() if report_summary['Number of Other Included Managers'] else 'N/A',
        report_summary['Information Table Entry Total'].group(1).strip() if report_summary['Information Table Entry Total'] else 'N/A',
        report_summary['Information Table Value Total'].group(1).strip() if report_summary['Information Table Value Total'] else 'N/A'
    }
    
    other_managers = re.findall(
        r'No\.\s+(\d+)\s*[\r\n]+Form 13F File Number:\s*([\d\-]+)\s*[\r\n]+Name:\s*(.*?)\s*(?=<PAGE>|No\.|\Z)',
        text
    )
    extracted['List of other Included Managers'] = other_managers
    
    # Extract form 13F information table from the text
    info_table_start = text.find('<TABLE>')
    info_table_end = text.find('</DOCUMENT>')
    info_table = text[info_table_start:info_table_end] if info_table_start != -1 and info_table_end != -1 else ''
    
    # Preprocess and get frequency distribution
    _, words = preprocess_text(text)
    freq_dist = FreqDist(words)
    
    return extracted, freq_dist, info_table

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract relevant sections
    extracted_info, freq_dist, info_table = extract_info(content)
    
    return extracted_info, freq_dist, info_table

def main(directory):
    data = []

    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            extracted_info, freq_dist, info_table = parse_file(file_path)
            
            # Collect data for each file
            data.append({
                'File': filename,
                **extracted_info,
                'Information Table': info_table
            })
    
    # Create a DataFrame to hold the collected data
    df = pd.DataFrame(data)
    
    # Save DataFrame to a CSV file for further analysis
    df.to_csv('13f_filings_summary.csv', index=False)
    print("Data extraction complete. Summary saved to '13f_filings_summary.csv'.")

if __name__ == "__main__":
    # Change 'your_directory_path' to the path where your 13F files are located
    directory_path = './13F'
    main(directory_path)
