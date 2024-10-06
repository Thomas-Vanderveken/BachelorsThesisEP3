import pandas as pd
import re

# Load CSV file
csv_file = 'test2.csv'  # Replace with your actual CSV file path
df = pd.read_csv(csv_file)
number_iloc = 2
# Extract the 'Information Table' column
info_table_text = df['Information Table'].iloc[number_iloc]

def pop_trailing_zero(arr):
    def parse_number(value):
        """Convert a string to an integer, handling European formatting."""
        try:
            # Remove periods for thousands separators and commas for decimal points
            value = value.replace('.', '').replace(',', '.')
            return float(value)
        except ValueError:
            return None
    
    def is_x_greater_than_100(value):
        """Check if the parsed number is greater than 100."""
        number = parse_number(value)
        return number is not None and number > 0
    
    def has_x_before_last_three(array):
        """Check if there's a number > 100 before the last 3 elements."""
        return any(is_x_greater_than_100(x) for x in array[:-3])
    
    while len(arr) > 3 and arr[-1] == '0' and has_x_before_last_three(arr):
        arr.pop()
    
    return arr

def extract_values(text):
    # Extract all pipe-separated values
    matches = re.findall(r'\|(.*?)\|', text)
    values = []
    for match in matches:
        # Split the values by commas, strip any extra whitespace and return as a list
        if '||' in match:
            break
        values.append([val.strip() for val in match.split(',')])
    return values

values_list = extract_values(info_table_text)

# Function to clean and split numbers with extra spaces
def clean_and_split(data):
    cleaned_data = []
    for sublist in data:
        new_sublist = []
        for item in sublist:
            if item == '':
                item = '0'
            # Check if the item contains extra spaces
            if re.search(r'\s{2,}', item):  # Detects multiple spaces
                # Split by spaces and filter out empty strings
                split_items = [num for num in item.split() if num]
                new_sublist.extend(split_items)
            else:
                new_sublist.append(item)
        print(new_sublist)
        cleaned_data.append(pop_trailing_zero(new_sublist)[-3:])
    return cleaned_data

# Apply the function to the input data
cleaned_data = clean_and_split(values_list)

# Rebuild the information table text with cleaned data
def rebuild_text(original_text, cleaned_data):
    # Find all pipe-separated sections in the original text
    matches = re.finditer(r'\|(.*?)\|', original_text)
    updated_text = original_text
    # Replace each section with cleaned data
    for match, new_data in zip(matches, cleaned_data):
        old_text = match.group(0)
        new_text = f"|{', '.join(new_data)}|"
        updated_text = updated_text.replace(old_text, new_text, 1)
    return updated_text

# Original text (from CSV) to be replaced
original_text = df['Information Table'].iloc[number_iloc]

# Rebuild the text with cleaned data
updated_text = rebuild_text(original_text, cleaned_data)

# Print the updated text
print("Updated Information Table:")
print(updated_text)

# Save the updated text back to the DataFrame
df.at[number_iloc, 'Information Table'] = updated_text

# Save the DataFrame back to a CSV file
output_csv_file = 'updated_test2.csv'  # Specify the output CSV file path
df.to_csv(output_csv_file, index=False)

print(f"Updated data saved to {output_csv_file}")
