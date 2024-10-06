import pandas as pd
import re

def clean_and_format_table(info_table):
    lines = info_table.splitlines()
    joined_lines = []
    
    # Join lines where the continuation starts with a space
    for line in lines:
        if line.startswith(' '):
            line = line.lstrip()
            if joined_lines:
                joined_lines[-1] += " " + line
            else:
                joined_lines.append(line)
        else:
            joined_lines.append(line)
    
    formatted_lines = []
    for line in joined_lines:
        # Remove lines with four or more consecutive dashes
        if re.search(r'-{4,}', line):
            continue
        # Remove lines containing HTML-like tags
        if re.search(r'<.*?>', line) and '</TABLE>' not in line:
            continue
        
        # Remove empty lines
        if not line.strip():
            continue
        
        # Find the first number longer than 3 digits
        match = re.search(r'\b[A-Za-z]*\d[A-Za-z\d]*\d[A-Za-z\d]*\d[A-Za-z\d]*\d[A-Za-z\d]*\d[A-Za-z\d]*\b', line)
        if match:
            number_start = match.start()
            # Split the line into two parts: before the number and after
            part_before_number = line[:number_start].rstrip()
            part_after_number = line[number_start:].lstrip()

            # Pad part_before_number to ensure part_after_number starts at column 80
            padding_needed = 80 - len(part_before_number)
            if padding_needed > 0:
                formatted_line = f"{part_before_number}{' ' * padding_needed}{part_after_number}"
            else:
                formatted_line = line
        else:
            formatted_line = line
        
        formatted_lines.append(formatted_line)
    
    return '\n'.join(formatted_lines)

def process_csv(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Process each row in the "Information Table" column
    df['Information Table'] = df['Information Table'].apply(clean_and_format_table)
    
    # Optionally, save the results to a new CSV file
    df.to_csv(output_csv, index=False)

# Usage
input_csv = './13f_filings_summary.csv'  # Path to your input CSV file
output_csv = 'test-temp.csv'  # Path to the output CSV file

process_csv(input_csv, output_csv)


import csv

# Input and test file names
input_csv = 'test-temp.csv'
output_csv = 'test.csv'

# Column name to modify
column_name = 'Information Table'

# Open the input CSV file for reading
with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    
    # Prepare to write the modified data to a new CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        
        # Write the header to the output file
        writer.writeheader()
        
        # Iterate over each row in the input CSV
        for row in reader:
            # Replace all commas in the specified column with an empty string
            if column_name in row:
                row[column_name] = row[column_name].replace(',', '')
            
            # Write the modified row to the output CSV
            writer.writerow(row)

print(f"Finished processing. Modified CSV saved as {output_csv}.")
