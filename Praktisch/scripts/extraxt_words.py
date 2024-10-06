import re
import csv
from extract_numbers import extract_number
text_block = """
ABN AMRO HOLDING NV ADR                  Common                                 937102   27486     1497900   SH     SOLE           1424355            73545
ABN AMRO HOLDING NV ADR                  Common                                 937102     322       17530   SH     UNKNOWN          17530
ACMAT CORP CLASS A       Common                                                 4616207     490       51890   SH     SOLE             51890
AKZO NOBEL NV SPONSORED ADR           ADR                                       10199305   31141      752646   SH     SOLE            721408            31238
AKZO NOBEL NV SPONSORED ADR           ADR                                       10199305      84        2030   SH     UNKNOWN           2030
ALAMO GROUP INC          Common                                                 11311107    2293      160348   SH     SOLE            159148             1200
AMERICAN ATLANTIC COMPANY                 Common                                24022105    2223      169342   SH     SOLE            169342
AMERICAN EXPRESS COMPANY      U           Common                                 25816109  158305     3833056   SH     SOLE           3716471           116585"""
def extract_info(text):
    # Define a regex pattern to match the CIK (alphanumeric string with no spaces)
    cik_pattern = re.compile(r'(?=.*\d)[A-Z0-9]{8,10}', re.IGNORECASE)
    
    # Normalize multiple spaces to a single space
    normalized_text = re.sub(r' {2,}', '  ', text).strip()
    print("Normalized Text:", normalized_text)
    
    # Split the text into parts based on double spaces
    parts = normalized_text.split('  ')
    
    # Initialize variables
    company_name = ""
    ticker = ""
    cik = ""
    number_sequence = ""
    temporary_number_sequence = ""
    
    # Iterate through the parts to find CIK and ticker
    for i, part in enumerate(parts):
        if cik_pattern.match(part):
            cik = parts[i]

            # Extract ticker (it's always right before the CIK)
            ticker = " ".join(parts[i-1:i])
            company_name = " ".join(parts[:i-1])
            
            # Extract numbers following the CIK
            numbers_after_cik = re.findall(r'\b\d+\b', " ".join(parts[i+1:]))
            if len(numbers_after_cik) >= 2:
                # Take the first two numbers
                number_sequence = " ".join(numbers_after_cik[:2])
                
                # If there are 5 or 6 numbers in total after the CIK, get the last three
                if len(numbers_after_cik) >= 5:
                    temporary_numbers = list(map(int, numbers_after_cik[-3:]))
                    temporary_number_sequence = " ".join(map(str, temporary_numbers))
                    
                    # Calculate the sum of the last three numbers
                    temp_sum = sum(temporary_numbers)
                    
                    # Reorder the number sequence
                    # We need to ensure the number equal to the sum is second in the sequence
                    numbers_to_reorder = numbers_after_cik[:2] + numbers_after_cik[2:-3]
                    if str(temp_sum) in numbers_to_reorder:
                        numbers_to_reorder.remove(str(temp_sum))
                        numbers_to_reorder.insert(1, str(temp_sum))
                    
                    number_sequence = " ".join(numbers_to_reorder)
            break
    
    # If the conditions for temporary_number_sequence are not met, execute Script A
    if not temporary_number_sequence:
        list_temporary_numbers = execute_script_a(text)
    
    return company_name, ticker, cik, number_sequence, temporary_number_sequence

def execute_script_a(textblock):
    return extract_number(text_block)
    
    

def write_to_csv(data, filename='results.csv'):
    # Append the extracted information to a CSV file
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # If the file is empty, write the header
        if file.tell() == 0:
            writer.writerow(['Company Name', 'Ticker', 'CIK', 'Number Sequence', 'Temporary Number Sequence'])
        # Write the data
        writer.writerow(data)

# Function to process each line and write results to CSV
def process_lines(lines):
    list_temporary_numbers = execute_script_a(text)
    
    for line in lines:

        company_name, ticker, cik, number_sequence, temporary_number_sequence = extract_info(line)
        print(f"Line: {line.strip()}")
        print(f"Company Name: {company_name}")
        print(f"Ticker: {ticker}")
        print(f"CIK: {cik}")
        print(f"Number Sequence: {number_sequence}")
        print(f"Temporary Number Sequence: {temporary_number_sequence}")
        print("---")
        
        # Write each result to the CSV
        write_to_csv([company_name, ticker, cik, number_sequence, temporary_number_sequence])

# Sample multiline text block

# Split the text block into lines
lines = text_block.strip().split('\n')

# Process each line and write results to CSV
process_lines(lines)
