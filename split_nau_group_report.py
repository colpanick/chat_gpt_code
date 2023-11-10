from pathlib import Path

def parse_user_report(input_file):
    input_path = Path(input_file)

    with open(input_path, 'r') as file:
        lines = file.readlines()

    current_group = None
    group_content = []

    for line in lines:
        if line.startswith("User group:"):
            break

        if not line.startswith(" "):
            if current_group:
                save_group_data(current_group, group_content, input_path.parent)
            current_group = line.strip()
            group_content = [line]
        else:
            group_content.append(line)

    # Save the last group if any
    if current_group:
        save_group_data(current_group, group_content, input_path.parent)

def save_group_data(group_name, group_content, output_directory):
    output_path = output_directory / f"{group_name}.txt"
    with open(output_path, 'w') as output_file:
        output_file.writelines(group_content)

if __name__ == "__main__":
    input_report = input("Enter the name of the user report file: ")
    parse_user_report(input_report)
    print("Parsing complete.")