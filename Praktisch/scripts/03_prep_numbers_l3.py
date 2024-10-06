import csv
import re

def find_pipe_positions(lines):
    earliest_position = float('inf')
    latest_position = -1
    
    for line in lines:
        last_letter_index = len(line) - 1
        while last_letter_index >= 0 and not line[last_letter_index].isalpha():
            last_letter_index -= 1
        
        # Adjusted regex to match integers and floating-point numbers
        match = re.search(r'\d+(\.\d+)?', line[last_letter_index + 1:])
        if match:
            number_start_index = last_letter_index + 1 + match.start()
            earliest_position = min(earliest_position, number_start_index)
            latest_position = max(latest_position, number_start_index)
    
    return earliest_position, latest_position

def process_lines_at_positions(lines, first_position, max_last_position):
    result = []
    for line in lines:
        # Adjust line with a pipe at the earliest position
        modified_line = line[:first_position] + '|' + line[first_position:]
        
        # Extend the line to max_last_position with spaces if needed
        if len(modified_line) < max_last_position:
            modified_line = modified_line.ljust(max_last_position)
        
        # Insert the final pipe at max_last_position
        modified_line = modified_line[:max_last_position] + '|'
        
        # Apply the comma insertion rule only between the pipes
        modified_line = insert_comma_between_pipes(modified_line)
        
        # Apply the ,0| or ,..| rule before the last pipe
        if max_last_position > 0:
            if modified_line[max_last_position - 1].isdigit():
                # If there is a number directly before the last pipe
                modified_line = re.sub(r'(\d+(\.\d+)?)\|$', r',\1|', modified_line)
            else:
                # If there's no number or non-digit before the last pipe
                modified_line = modified_line[:-1] + '|'
        
        result.append(modified_line)
    return result

def insert_comma_between_pipes(line):
    # Find the first and last pipe positions
    first_pipe_pos = line.find('|')
    last_pipe_pos = line.rfind('|')
    
    if first_pipe_pos != -1 and last_pipe_pos != -1 and first_pipe_pos < last_pipe_pos:
        # Extract the part between the pipes
        between_pipes = line[first_pipe_pos + 1:last_pipe_pos]
        
        # Insert comma after a number > 0 followed by spaces (but not a comma)
        modified_between_pipes = re.sub(r'(\d+(\.\d+)(\.\d+)?)(\s*)(?![,|])', r'\1,\3', between_pipes)
        
        # Reconstruct the line with the modified section
        line = line[:first_pipe_pos + 1] + modified_between_pipes + line[last_pipe_pos:]
    
    return line

def modify_line(line, position):
    if position != -1 and position + 1 < len(line):
        after_pipe = line[position + 1:]
        if after_pipe and (after_pipe[0].isdigit() or after_pipe[0] == '.'):
            match = re.match(r'\d+(\.\d+)?', after_pipe)
            if match:
                number_end_index = match.end()
                return line[:position + number_end_index + 1] + ',' + line[position + number_end_index + 1:]
    
    return line[:position + 1] + ',' + line[position + 1:]

def process_section(section):
    lines = section.splitlines()
    first_pipe_index, _ = find_pipe_positions(lines)
    
    # Determine the maximum position among all lines in the section
    max_last_position = max(len(line) for line in lines)+1
    
    lines = process_lines_at_positions(lines, first_pipe_index, max_last_position)
    modified_lines = [modify_line(line, first_pipe_index) for line in lines]
    
    # Join lines and handle double commas as the last step
    joined_lines = '\n'.join(modified_lines)
    return remove_double_commas(joined_lines)

def remove_double_commas(text):
    # Replace any sequence of consecutive commas with a single comma
    return re.sub(r',+', ',', text)

def split_into_sections(data, end_tag="</TABLE>"):
    sections = data.split(end_tag)
    return [section + end_tag for section in sections[:-1]] + [sections[-1]] if sections[-1].strip() else sections[:-1]

def process_csv_section_by_section(input_csv_path, output_csv_path):
    with open(input_csv_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    modified_rows = []
    for row in rows:
        column_to_modify = row['Information Table']  # Assuming 'Information Table' is the column to modify
        sections = split_into_sections(column_to_modify)
        
        processed_sections = []
        for section in sections:
            processed_section = process_section(section)
            processed_sections.append(processed_section)
        
        row['Information Table'] = ''.join(processed_sections)
        modified_rows.append(row)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(modified_rows)

# Example usage
input_csv_path = 'test.csv'  # Path to your CSV file
output_csv_path = 'test2.csv'  # Path for the output CSV file
process_csv_section_by_section(input_csv_path, output_csv_path)
