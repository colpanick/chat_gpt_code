from pathlib import Path
import csv

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

# Find differences in old dip files
in_old_not_in_new = old_unique_values - new_unique_values
output_file_path_old = OUTPUT_DIRECTORY / f"{DIP_PREFIX}-old-differences.csv"
with open(output_file_path_old, 'w', newline='') as output_file_old:
    csv_writer_old = csv.writer(output_file_old)
    csv_writer_old.writerow(["Filepath", "ID"])
    for file_path in OLD_DIP_LOCATION.glob(f"{DIP_PREFIX}*.txt"):
        header, rows = extract_rows_by_ids(file_path, ID_COLUMN, in_old_not_in_new)
        if rows:
            csv_writer_old.writerows(rows)

# Find differences in new dip files
in_new_not_in_old = new_unique_values - old_unique_values
output_file_path_new = OUTPUT_DIRECTORY / f"{DIP_PREFIX}-new-differences.csv"
with open(output_file_path_new, 'w', newline='') as output_file_new:
    csv_writer_new = csv.writer(output_file_new)
    csv_writer_new.writerow(["Filepath", "ID"])
    for file_path in NEW_DIP_LOCATION.glob(f"{DIP_PREFIX}*.txt"):
        header, rows = extract_rows_by_ids(file_path, ID_COLUMN, in_new_not_in_old)
        if rows:
            csv_writer_new.writerows(rows)

print(f"Differences in old dip files written to: {output_file_path_old}")
print(f"Differences in new dip files written to: {output_file_path_new}")
