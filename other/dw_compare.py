import csv

def compare_csv_files(file1, file2, column_number, output_columns, output_file):
    data1 = read_csv(file1)
    data2 = read_csv(file2)

    column_values1 = set(row[column_number] for row in data1)
    column_values2 = set(row[column_number] for row in data2)

    unique_values_in_file1 = column_values1 - column_values2
    unique_values_in_file2 = column_values2 - column_values1

    unique_rows = [row for row in data1 if row[column_number] in unique_values_in_file1]
    unique_rows += [row for row in data2 if row[column_number] in unique_values_in_file2]

    write_csv(unique_rows, output_columns, output_file)

def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return [row for row in reader]

def write_csv(data, columns, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows([row[col] for col in columns] for row in data)

if __name__ == "__main__":
    file1_path = "file1.csv"
    file2_path = "file2.csv"
    column_number = 1  # Change to the desired column number (0-based index)
    output_columns = ["Column1", "Column2", "Column3"]  # Change to the desired column names
    output_file_path = "output_file.csv"

    compare_csv_files(file1_path, file2_path, column_number, output_columns, output_file_path)