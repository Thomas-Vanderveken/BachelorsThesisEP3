import re
from prep import proces
# input_text = """
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
# CREDIT ACCEPTANCE CORP-MICH               Common                                225310101    6084     1145251   SH     SOLE           1141886             3365"""
def extract_number(input_text):
    def extract_values(text):
        # Extract the content between the first and second pipe '|'
        match = re.search(r'\|(.*?)\|', text)
        if match:
            # Split the values by commas, strip any extra whitespace and return as a list
            return [val.strip() for val in match.group(1).split(',')]
        return []


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
            cleaned_data.append(new_sublist)
        return cleaned_data

    input_text = proces(input_text)
    values_list = []
    # Process each line in the data
    for line in input_text.strip().split('\n'):
        values = extract_values(line)
        # print(values)
        values_list.append(values)

    # print("-" * 50)
    # Apply the function to the input data
    cleaned_data = clean_and_split(values_list)

    # # Print the cleaned data
    # for line in cleaned_data:
    #     print(line[-3:])

    print(cleaned_data)
    return cleaned_data