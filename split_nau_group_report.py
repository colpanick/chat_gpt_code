import os

def process_document(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    current_document = None
    document_content = []

    for line in lines:
        if line.strip():  # Check if the line is not empty or whitespace only
            if current_document:
                document_content.append(line)
            else:
                current_document = line.strip()
                document_content = [line]

        elif current_document:
            # Save the content to a file
            save_document(current_document, document_content)
            current_document = None
            document_content = []

    # Save the last document if any
    if current_document:
        save_document(current_document, document_content)

def save_document(document_name, document_content):
    output_directory = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(output_directory, f"{document_name}.txt")

    with open(output_file_path, 'w') as output_file:
        output_file.writelines(document_content)

if __name__ == "__main__":
    input_document = input("Enter the path of the document to process: ")
    process_document(input_document)
    print("Processing complete.")
