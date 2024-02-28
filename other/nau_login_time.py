import csv
import re
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
LOG_FILE_PATH = Path("/path/to/logfile.txt")
OUTPUT_CSV_PATH = Path("/path/to/output.csv")

# Function to convert time string to minutes
def convert_time_to_minutes(time_str):
    time_components = [int(x) for x in time_str.split(":")]
    return time_components[0] * 60 + time_components[1]

# Function to calculate the duration in minutes between two time strings
def calculate_duration_in_minutes(start_time_str, end_time_str):
    start_time_minutes = convert_time_to_minutes(start_time_str)
    end_time_minutes = convert_time_to_minutes(end_time_str)
    return end_time_minutes - start_time_minutes

# Function to extract the workstation name from the message
def extract_workstation_name(message):
    match = re.search(r'Wkst\s+(.+)', message)
    return match.group(1) if match else None

# Function to parse the log file and calculate total minutes logged for each user each day
def parse_log_and_generate_csv(log_file_path, output_csv_path):
    data = []
    active_sessions = {}  # Dictionary to track active sessions for each user

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if line.startswith("Date:"):
                current_date = datetime.strptime(line.split()[1], "%m/%d/%Y").date()
                active_sessions = {}  # Reset active sessions for each new date
            elif "Logged into Client Module" in line:
                current_user = line[14:44].strip()
                login_time = line[5:13].strip()
                message = line[45:].strip()
                workstation_name = extract_workstation_name(message)
                active_sessions[current_user] = {"login_time": login_time, "logout_time": None, "workstation": workstation_name}
            elif "Logged out of Client Module" in line:
                current_user = line[14:44].strip()
                logout_time = line[5:13].strip()
                message = line[45:].strip()
                workstation_name = extract_workstation_name(message)
                if current_user in active_sessions and active_sessions[current_user]["logout_time"] is None:
                    active_sessions[current_user]["logout_time"] = logout_time
                    duration = calculate_duration_in_minutes(active_sessions[current_user]["login_time"], logout_time)
                    data.append((current_date, current_user, duration, workstation_name))

    # Create a CSV file with the results
    with open(output_csv_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter='|')
        csv_writer.writerow(["Date", "Login ID", "Total Minutes logged into system", "Workstation"])
        for entry in data:
            csv_writer.writerow(entry)

def main():
    parse_log_and_generate_csv(LOG_FILE_PATH, OUTPUT_CSV_PATH)

if __name__ == "__main__":
    main()