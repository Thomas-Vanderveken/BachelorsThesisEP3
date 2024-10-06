import pandas as pd
import re

def clean_and_format_table(info_table):
    lines = info_table.splitlines()
    joined_lines = []
    
    # Join lines where the continuation starts with a space
    for line in lines:
        if line.startswith(' '):  # If the line starts with a space, join it with the previous line
            if joined_lines:
                joined_lines[-1] += line  # Join the current line with the last line in joined_lines
        else:
            joined_lines.append(line)  # Add the current line to joined_lines
    
    formatted_lines = []
    for line in joined_lines:
        # Remove lines with three consecutive dashes
        if re.search(r'-{4,}', line):
            continue
        # Remove lines containing HTML-like tags
        if re.search(r'<.*?>', line) and '</TABLE>' not in line:
            continue
        
        # Remove empty lines
        if not line.strip():
            continue
        
        # Find the position of the first two consecutive spaces
        first_two_spaces_index = line.find('  ')
        if first_two_spaces_index != -1:
            # Ensure that the text after the first two spaces starts at column 40
            part_before_spaces = line[:first_two_spaces_index + 2].rstrip()
            part_after_spaces = line[first_two_spaces_index + 2:].lstrip()
            
            # Pad part_after_spaces to start at column 40
            formatted_line = f"{part_before_spaces:<39} {part_after_spaces}"
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
output_csv = 'test.csv'  # Path to the output CSV file

process_csv(input_csv, output_csv)
