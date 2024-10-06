import re

def find_pipe_positions(lines):
    earliest_position = float('inf')
    latest_position = -1
    
    for line in lines:
        # Finding the position after the last letter in the line
        last_letter_index = len(line) - 1
        while last_letter_index >= 0 and not line[last_letter_index].isalpha():
            last_letter_index -= 1
        
        # Find the position where the first number starts after the last letter
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
                modified_line = modified_line[:-1] + ',|'
        
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
        modified_between_pipes = re.sub(r'(\d+(\.\d+)?)(\s+)(?![,|])', r'\1,\3', between_pipes)
        
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

def process_lines(lines):
    lines = lines.strip().splitlines()  # Split the input into individual lines

    lines = [line + ',0,0,0' if line.rstrip().endswith("SOLE") else line for line in lines]

    first_pipe_index, _ = find_pipe_positions(lines)
    
    # Determine the maximum position among all lines
    max_last_position = max(len(line) for line in lines) + 1
    
    lines = process_lines_at_positions(lines, first_pipe_index, max_last_position)
    modified_lines = [modify_line(line, first_pipe_index) for line in lines]
    
    # Join lines and handle double commas as the last step
    joined_lines = '\n'.join(modified_lines)
    return remove_double_commas(joined_lines)

def remove_double_commas(text):
    # Replace any sequence of consecutive commas with a single comma
    return re.sub(r',+', ',', text)

# Example usage
# lines = """
# BRISTOL MEYERS SQUIBB CO               Common                                   110122108   36791      619375   SH     SOLE            591895            27480
# BRISTOL MEYERS SQUIBB CO               Common                                   110122108     336        5655   SH     UNKNOWN           5655
# CCBT FINANCIAL COMPANIES INC           Common                                   12500Q102     446       20400   SH     SOLE             20400
# CHARTER ONE FINANCIAL INC.                    Common                            160903100     494       17465   SH     SOLE             17465
# COCA COLA BOTTLING COMPANY                 Common                               191098102    9940      245818   SH     SOLE            245408              410
# COCA COLA BOTTLING COMPANY                 Common                               191098102       5         128   SH     UNKNOWN            128
# COMCAST CORP SPECIAL CLASS A                 CL A                               200300200   63002     1502274   SH     SOLE           1466434            35840
# COMCAST CORP SPECIAL CLASS A                 CL A                               200300200      49        1173   SH     UNKNOWN           1173
# COMERICA INCORPORATED    Common                                                 200340107   29455      478948   SH     SOLE            478756              192
# COMMONWEALTH TELEPHONE ENTERPRISES             Common                           203349105   16186      469165   SH     SOLE            468112             1053
# COMMONWEALTH TELEPHONE ENTERPRISES             Common                           203349105     120        3483   SH     UNKNOWN           3483
# COMMUNITY FINANCIAL GROUP INC.              Common                              20365M108     789       59825   SH     SOLE             59825
# COMMUNITY FINANCIAL GROUP INC.              Common                              20365M108      52        3945   SH     UNKNOWN           3945
# CREDIT ACCEPTANCE CORP-MICH               Common                                225310101    6084     1145251   SH     SOLE           1141886             3365
#     """

def proces(lines):
    processed_output = process_lines(lines)
    return processed_output