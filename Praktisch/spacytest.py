import re

def process_input(text):
    # Split text into lines and concatenate short lines with the next line
    lines = text.strip().split('\n')
    merged_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        if len(line) < 25 and i + 1 < len(lines):
            line += ' ' + lines[i + 1].strip()
            i += 1
        merged_lines.append(line)
        i += 1
    
    result_lines = []
    for line in merged_lines:
        # Split based on multiple spaces
        columns = re.split(r'\s{2,}', line)
        
        # Ensure the first column is quoted
        if columns:
            columns[0] = f'"{columns[0].strip()}"'
        
        # Handle the irregularities in the last three columns
        if len(columns) < 9:
            # Add 0s for missing columns in the last 3 columns
            columns.extend(['0'] * (9 - len(columns)))
        elif len(columns) > 9:
            # Adjust if there are more than 9 columns by separating the last 3 columns
            columns = columns[:8] + [columns[8]] + ['0'] * (len(columns) - 9) + [columns[-1]]
        
        # Ensure exactly 9 columns, with the last 3 columns separated
        if len(columns) > 9:
            columns = columns[:8] + columns[8:] + ['0'] * (9 - len(columns))
        
        # Format the output
        result_line = ','.join(columns)
        result_lines.append(result_line)
    
    return '\n'.join(result_lines)

# Example input
#TODO change a , to .
input_text = [

    "NV ADR                  Common             937102   27486     1497900   SH     SOLE           |1424355,                ,|",
    "NV ADR                  Common             937102   27486     1497900   SH     SOLE           |,          73545        ,|",
    "NV ADR                  Common             937102   27486     1497900   SH     SOLE           |,                  ,73545|",
    "NV ADR                  Common             937102   27486     1497900   SH     SOLE           |1424355,           ,73545|",
    "NV ADR                  Common             937102   27486     1497900   SH     SOLE           |1424355,  73545         ,|",
    "COCA COLA CO                   COM              191216100      485    10098 SH       SOLE                    |10098,        0        ,0|",
    "COLGATE PALMOLIVE CO           COM              194162103     1407    19895 SH       SOLE                    |19895,        0        ,0|",
    "COMCAST CORP NEW               CL A             20030N101      154    10673 SH       SOLE                    |10673,        0        ,0|",
    "Aegis Realty Inc.                        COM      00760P104     7,200      81    X                              |7.200,    0         ,0|",
    "Agere Systems Inc. CL B                 CL B      00845V209       2         0    X                              |,   10        0     ,2|",
    
"Alcatel-Lucent                 SPONSORED ADR  013904305      475   291,367 SH       SOLE       |0,               291.367    ,0|",
"Alcoa Inc                      Common         013817101      309    35,283 SH       SOLE       |0,    0          35.283     ,0|",

"Adtran (ADTN)                  COM              00738A106     6023   155600 SH       SOLE                   |0, 99300          ,56300|",
"Agilent Technologies (A)       COM              00846U101    10968   214600 SH       SOLE                   |0, 103400            ,111200|",

"ISHARES TR                     RUSSELL1000GRW   464287614    52731   866141 SH       SOLE                        |0,        0   ,866141|",
"ISHARES TR                     RUSL 2000 VALU   464287630     1357    18486 SH       SOLE                        |0,        0    ,18486|",

"AUTOMATIC DATA PROCESSIN	COMMON		053015103  185140  3514433 SH		SOLE		|,	0  3391733  ,122700|",
"AVON PRODS INC			COMMON		054303102   80208  2864583 SH		SOLE			|0,  2766433  0 ,98150|",
]

# Process the input and print the output
# output = process_input(input_text)
# print(output)
def extract_values(text):
    # Extract the content between the first and second pipe '|'
    match = re.search(r'\|(.*?)\|', text)
    if match:
        # Split the values by commas, strip any extra whitespace and return as a list
        return [val.strip() for val in match.group(1).split(',')]
    return []
values_list=[]
# Process each line in the data
for line in input_text:
    values = extract_values(line)
    print(values)
    values_list.append(values)

print("-"*50)


# Function to clean and split numbers with extra spaces
def clean_and_split(data):
    cleaned_data = []
    for sublist in data:
        new_sublist = []
        for item in sublist:
            if item == '':
                item='0'
            # Check if the item contains extra spaces
            if re.search(r'\s{2,}', item):  # Detects multiple spaces
                # Split by spaces and filter out empty strings
                split_items = [num for num in item.split() if num]
                new_sublist.extend(split_items)
            else:
                new_sublist.append(item)
        cleaned_data.append(new_sublist)
    return cleaned_data

# Apply the function to the input data
cleaned_data = clean_and_split(values_list)

# Print the cleaned data
print(cleaned_data)
print(values_list)

for line in cleaned_data:
    print(line[-3:])