import csv
import re
from datetime import datetime
import sqlite3
from pathlib import Path
import os

# Configuration
LOG_FILE_PATH = Path("/path/to/logfile.txt")
OUTPUT_CSV_PATH = Path("/path/to/output.csv")
DATABASE_PATH = Path("tmp.db")

# Function to convert time string to minutes
def convert_time_to_minutes(time_str):
    time_components = [int(x) for x in time_str.split(":")]
    return time_components[0] * 60 + time_components[1]

# Function to extract the workstation name from the message
def extract_workstation_name(message):
    match = re.search(r'Wkst\s+(.+)', message)
    return match.group(1) if match else None

# Function to create SQLite database and table
def create_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create a table to store log data
    cursor.execute('''CREATE TABLE IF NOT EXISTS log_data (
                        login_date TEXT,
                        login_time TEXT,
                        user_id TEXT,
                        workstation TEXT,
                        login_out TEXT
                    )''')

    conn.commit()
    conn.close()

# Function to parse the log file and upload data to SQLite database
def parse_log_and_upload_to_database(log_file_path):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if line.startswith("Date:"):
                current_date = datetime.strptime(line.split()[1], "%m/%d/%Y").date()
            elif "Logged into Client Module" in line:
                current_user = line[14:44].strip()
                login_time = line[5:13].strip()
                message = line[45:].strip()
                workstation_name = extract_workstation_name(message)
                cursor.execute("INSERT INTO log_data VALUES (?, ?, ?, ?, 'login')", (current_date, login_time, current_user, workstation_name))
            elif "Logged out of Client Module" in line:
                current_user = line[14:44].strip()
                logout_time = line[5:13].strip()
                message = line[45:].strip()
                workstation_name = extract_workstation_name(message)
                cursor.execute("INSERT INTO log_data VALUES (?, ?, ?, ?, 'logout')", (current_date, logout_time, current_user, workstation_name))

    conn.commit()
    conn.close()

# Function to calculate total minutes logged for each user each day
def calculate_total_minutes_logged():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Sort the table by date and time ascending
    cursor.execute("SELECT * FROM log_data ORDER BY login_date ASC, login_time ASC")

    data = []
    active_sessions = {}  # Dictionary to track active sessions for each user

    for row in cursor.fetchall():
        login_date, login_time, current_user, workstation_name, login_out = row
        if login_out == 'login':
            active_sessions[current_user] = {"login_time": login_time, "workstation": workstation_name}
        elif login_out == 'logout' and current_user in active_sessions:
            logout_time = login_time
            duration = convert_time_to_minutes(logout_time) - convert_time_to_minutes(active_sessions[current_user]["login_time"])
            data.append((login_date, current_user, duration, active_sessions[current_user]["workstation"]))
            del active_sessions[current_user]

    conn.close()

    # Create a CSV file with the results
    with open(OUTPUT_CSV_PATH, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter='|')
        csv_writer.writerow(["Date", "Login ID", "Total Minutes logged into system", "Workstation"])
        for entry in data:
            csv_writer.writerow(entry)

# Function to remove the temporary SQLite database
def remove_temporary_database():
    if DATABASE_PATH.exists():
        os.remove(DATABASE_PATH)

def main():
    create_database()
    parse_log_and_upload_to_database(LOG_FILE_PATH)
    calculate_total_minutes_logged()
    remove_temporary_database()

if __name__ == "__main__":
    main()