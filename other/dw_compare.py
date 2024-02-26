from pathlib import Path
import csv
import shutil

# Configuration
OLD_DIP_LOCATION = Path("/path/to/old/directory")
NEW_DIP_LOCATION = Path("/path/to/new/directory")
DIP_PREFIX = "your_prefix"
ID_COLUMN = 2  # Assuming 0-based indexing for columns
OUTPUT_DIRECTORY = Path("/path/to/output/directory")

# Function to parse a CSV file and extract rows with specific IDs
def extract_rows_by_ids(file_path, column_index, target_ids):
    rows = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter='|')
        header = next(reader)  # Skip header
        for row in reader:
            if row[column_index] in target_ids:
                rows.append((file_path, row))
    return header, rows

# Get unique values from OLD_DIP_LOCATION
old_unique_values = set()
for file_path in OLD_DIP_LOCATION.glob(f"{DIP_PREFIX}*.txt"):
    old_unique_values.update(extract_unique_values(file_path, ID_COLUMN))

# Get unique values from NEW_DIP_LOCATION
new_unique_values = set()
for file_path in NEW_DIP_LOCATION.glob(f"{DIP_PREFIX}*.txt"):
    new_unique_values.update(extract_unique_values(file_path, ID_COLUMN))

# Find differences
in_old_not_in_new = old_unique_values - new_unique_values
in_new_not_in_old = new_unique_values - old_unique_values

# Create the first output file
output_file_path = OUTPUT_DIRECTORY / f"{DIP_PREFIX}-differences.csv"
with open(output_file_path, 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["Filepath", "ID"])
    for file_path in OLD_DIP_LOCATION.glob(f"{DIP_PREFIX}*.txt"):
        header, rows = extract_rows_by_ids(file_path, ID_COLUMN, in_old_not_in_new)
        if rows:
            csv_writer.writerows(rows)

# Parse the first output file and extract the entire record
output_records = []
with open(output_file_path, 'r') as output_file:
    csv_reader = csv.reader(output_file)
    header = next(csv_reader)  # Skip header
    for row in csv_reader:
        file_path, record_id = row
        with open(file_path, 'r') as dip_file:
            dip_reader = csv.reader(dip_file, delimiter='|')
            for dip_row in dip_reader:
                if dip_row[ID_COLUMN] == record_id:
                    output_records.append((file_path, dip_row))
                    break

# Create the second output file
output_records_file_path = OUTPUT_DIRECTORY / f"{DIP_PREFIX}-differences-records.csv"
with open(output_records_file_path, 'w', newline='') as output_records_file:
    csv_writer = csv.writer(output_records_file)
    csv_writer.writerow(["Filepath", "Record"])
    csv_writer.writerows(output_records)

print(f"Differences written to: {output_file_path}")
print(f"Corresponding records written to: {output_records_file_path}")