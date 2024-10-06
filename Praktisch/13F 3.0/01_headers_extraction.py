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
import re
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    return None, words  # Return words, ignoring the first returned value
import re
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    # Tokenize the text into words
    words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    return None, words  # Return words, ignoring the first returned value

def extract_info(text):
    # Define regex patterns to capture various fields
    fields = {
        'FileType': r"<TYPE>(.*)",
        'Filename': r"<FILENAME>(.*)",
        'Description': r"<DESCRIPTION>(.*)",
        'ReportDate': r"Report for the Calendar Year or Quarter Ended:\s*(.*)",
        'CompanyName': r"Institutional Investment Manager Filing this Report:\s*Name:\s*(.*)",
        'Address1': r"Address:\s*(.*)",
        'Address2': r'Address:[^\n]*\n\s*([^\n]+)',
        'FileNumber': r"File Number:\s*(.*)",
        'PersonName': r"Person Signing this Report on Behalf of (?:the )?Reporting Manager:\s*Name:\s*(.*)",
        'Title': r"Title:\s*(.*)",
        'Phone': r"Phone:\s*(.*)",
        'Signature': r"Signature\s*,\s*Place,\s*and\s*Date\s*of\s*Signing:\s*(.*)",
        'ReportType': r'\[\s*x\s*\]\s*(13F HOLDING[S]?\sREPORT|13F NOTICE|13F COMBINATION REPORT)'
    }
    
    # Extract fields with default 'N/A' if not found
    extracted = {key: (re.search(pattern, text, re.IGNORECASE).group(1).strip() if re.search(pattern, text, re.IGNORECASE) else 'N/A') for key, pattern in fields.items()}
    address1 = extracted.get('Address1', 'N/A')
    address2 = extracted.get('Address2', 'N/A')
    if address1 == 'N/A' and address2 == 'N/A':
        extracted['Address'] = 'N/A'
    elif address1 == address2:
        extracted['Address'] = f"{address1}".strip()
    else:
        extracted['Address'] = f"{address1} {address2}".strip()
    
    # Remove Address1 and Address2 from the dictionary since they're now merged
    extracted.pop('Address1', None)
    extracted.pop('Address2', None)

    # Extract summary fields with default 'N/A' if not found
    report_summary = {
        'NumberOfOtherIncludedManagers': re.search(r'Number\s*of\s*Other\s*Included\s*Managers\s*:\s*(\d+)\s*', text, re.IGNORECASE),
        'InformationTableEntryTotal': re.search(r'Form\s*13F\s*Information\s*Table\s*Entry\s*Total\s*:\s*(\d+)\s*', text, re.IGNORECASE),
        'InformationTableValueTotal': re.search(r'Form\s*13F\s*Information\s*Table\s*Value\s*Total\s*:\s*\$([\d,]+)', text, re.IGNORECASE)
    }
    
    # Update extracted dictionary with report summary fields, ensuring they are plain numbers (strings)
    extracted['NumberOfOtherIncludedManagers'] = report_summary['NumberOfOtherIncludedManagers'].group(1).strip() if report_summary['NumberOfOtherIncludedManagers'] else 'N/A'
    extracted['InformationTableEntryTotal'] = report_summary['InformationTableEntryTotal'].group(1).strip() if report_summary['InformationTableEntryTotal'] else 'N/A'
    extracted['InformationTableValueTotal'] = report_summary['InformationTableValueTotal'].group(1).strip() if report_summary['InformationTableValueTotal'] else 'N/A'

    # Extract list of other included managers
    other_managers = re.findall(
        r'No\.\s+(\d+)\s*[\r\n]+Form 13F File Number:\s*([\d\-]+)\s*[\r\n]+Name:\s*(.*?)\s*(?=<PAGE>|No\.|\Z)',
        text
    )
    extracted['ListOfOtherIncludedManagers'] = other_managers if other_managers else None

    
    # Extract form 13F information table from the text
    info_table_start = text.find('<TABLE>')
    info_table_end = text.find('</DOCUMENT>')
    info_table = text[info_table_start:info_table_end] if info_table_start != -1 and info_table_end != -1 else ''
    
    # Preprocess text and get frequency distribution
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
                # 'InformationTable': info_table
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
