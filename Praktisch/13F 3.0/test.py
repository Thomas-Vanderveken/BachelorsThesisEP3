from extraxt_words import get_values
import csv

def process_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:  # Specify encoding if necessary
        csv_reader = csv.DictReader(file)

        row_count = 0
        # Iterate over the rows in the CSV
        for row in csv_reader:
            row_count += 1
            print(f"Processing row {row_count}: {row}")  # Debug: Print current row

            # Access the "Information Table" column
            if "Information Table" in row:
                info_table = row["Information Table"]
                file_number = row["File Number"]
                print(f"Information Table content: {info_table}")  # Debug: Print content

                # Split the content into blocks by "<\Table>"
                blocks = info_table.split("<\\Table>")
                
                # Iterate over the blocks and pass each to the get_values function
                for i, block in enumerate(blocks):
                    block = block.strip()  # Clean up any leading/trailing whitespace
                    if block:  # Ensure the block isn't empty
                        print(f"Processing block {i + 1}/{len(blocks)} in row {row_count}")  # Debug: Print block info
                        print(file_number)
                        get_values(block, file_number)
            else:
                print(f"Warning: 'Information Table' column not found in row {row_count}")

# Example usage:
process_csv("./test.csv")
