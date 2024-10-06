import re
import csv
from extract_numbers import extract_number

def extract_info(text, l_temp):
    # Define a regex pattern to match the CIK (alphanumeric string with no spaces)
    cik_pattern = re.compile(r'^(?!.*\s)(?=.*\d)[A-Z0-9]{5,12}$', re.IGNORECASE)
    
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
            cik = part
            print('p', part)

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
        temporary_number_sequence = f"{l_temp[0]}, {l_temp[1]}, {l_temp[2]}"
        
    return company_name, ticker, cik, number_sequence, temporary_number_sequence



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
def process_lines(lines, list_temp_numbers):
    c = 0

    for line in lines:
        company_name, ticker, cik, number_sequence, temporary_number_sequence = extract_info(line, list_temp_numbers[0])
        # print(f"Line: {line.strip()}")
        # print(f"Company Name: {company_name}")
        # print(f"Ticker: {ticker}")
        # print(f"CIK: {cik}")
        # print(f"Number Sequence: {number_sequence}")
        # print(f"Temporary Number Sequence: {temporary_number_sequence}")
        # print("---")
        
        # Write each result to the CSV
        write_to_csv([company_name, ticker, cik, number_sequence, temporary_number_sequence])
        c+=1

# Sample multiline text block

def get_values(text):
    list_temporary_numbers = extract_number(text)
    
    lines = text.strip().split('\n')

    # Process each line and write results to CSV
    process_lines(lines, list_temporary_numbers)

text = """
ABN AMRO HOLDING NV ADR                  Common                                 937102     322       17530   SH     UNKNOWN          17530
ACMAT CORP CLASS A       Common                                                 4616207     490       51890   SH     SOLE             51890
LEVEL 3 COMMUNICATIONS INC                         Common                       52729N100     332       19100   SH         SOLE                      19000              100

"""
get_values(text)