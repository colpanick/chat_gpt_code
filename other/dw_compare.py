from pathlib import Path
import csv

# Configuration
OLD_DIP_LOCATION = Path("/path/to/old/directory")
NEW_DIP_LOCATION = Path("/path/to/new/directory")
DIP_PREFIX = "your_prefix"
ID_COLUMN = 2  # Assuming 0-based indexing for columns
OUTPUT_DIRECTORY = Path("/path/to/output/directory")

# Function to parse a CSV file and extract unique values in the specified column
def extract_unique_values(file_path, column_index):
    unique_values = set()
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='|')
        for row in reader:
            unique_values.add(row[column_index])
    return unique_values

# Get unique values from OLD_DIP_LOCATION
old_unique_values = set()
for file_path in OLD_DIP_LOCATION.glob(f"{DIP_PREFIX}*.txt"):
    old_unique_values.update(extract_unique_values(file_path, ID_COLUMN))

# Get unique values from NEW_DIP_LOCATION
new_unique_values = set()
for file_path in NEW_DIP_LOCATION.glob(f"{DIP_PREFIX}*.txt"):
    new_unique_values.update(extract_unique_values(file_path, ID_COLUMN))

# Find differences
differences = {
    "in_old_not_in_new": old_unique_values - new_unique_values,
    "in_new_not_in_old": new_unique_values - old_unique_values
}

# Write differences to the output file
output_file_path = OUTPUT_DIRECTORY / f"{DIP_PREFIX}-differences.txt"
with open(output_file_path, 'w') as output_file:
    for diff_type, values in differences.items():
        output_file.write(f"{diff_type}:\n")
        for value in values:
            output_file.write(f"{value}\n")
        output_file.write("\n")

print(f"Differences written to: {output_file_path}")
