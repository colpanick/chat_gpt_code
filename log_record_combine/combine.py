import csv
import re
import glob
import openpyxl


def process_log_file(
    log_file_path, glob_filters, excel_file_path, output_file_path, match_file_path=None
):
    try:
        # Load the Excel file
        workbook = openpyxl.load_workbook(excel_file_path)
        sheet = workbook.active
    except FileNotFoundError:
        print(f"Error: Could not find Excel file {excel_file_path}")
        return
    except openpyxl.utils.exceptions.InvalidFileException:
        print(f"Error: Excel file {excel_file_path} is invalid or corrupted")
        return

    try:
        # Open the output file for writing
        with open(output_file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file, delimiter="|")

            # Open the optional match file for appending
            if match_file_path:
                try:
                    match_file = open(match_file_path, "a")
                except FileNotFoundError:
                    print(f"Error: Could not find match file {match_file_path}")
                    match_file = None
            else:
                match_file = None

            try:
                # Loop through the log file and filter by glob
                with open(log_file_path, "r") as log_file:
                    for line in log_file:
                        if not any(
                            glob.fnmatch.fnmatch(line, filter)
                            for filter in glob_filters
                        ):
                            continue

                        # Extract the document ID from the log entry
                        match = re.search(r"ID: (\d+)", line)
                        if match:
                            document_id = match.group(1)

                            # Find the corresponding row in the Excel file
                            for row in sheet.iter_rows(
                                min_row=2, min_col=2, values_only=True
                            ):
                                if str(row[0]) == document_id:
                                    # Write the row from the Excel file and the log entry to the output file
                                    writer.writerow(row + (line.strip(),))

                                    # Write the log entry to the match file if specified
                                    if match_file:
                                        match_file.write(line)
            except FileNotFoundError:
                print(f"Error: Could not find log file {log_file_path}")
    except PermissionError:
        print(f"Error: Permission denied for output file {output_file_path}")
    finally:
        if match_file:
            match_file.close()
