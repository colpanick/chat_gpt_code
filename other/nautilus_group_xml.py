import xml.etree.ElementTree as ET
import csv

# Define the XML file path and CSV output file path
xml_file_path = 'your_xml_file.xml'
csv_file_path = 'output.csv'

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Initialize a list to store the extracted names
name_values = []

# Find all <Group> nodes within <Response>
response_node = root.find(".//Response")
if response_node is not None:
    group_nodes = response_node.findall(".//Group")
    for group_node in group_nodes:
        # Find the <Name> node within each <Group> node
        name_node = group_node.find(".//Name")
        if name_node is not None:
            name_values.append(name_node.text)

# Save the extracted names to a CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    for name in name_values:
        csv_writer.writerow([name])

print(f"Extracted {len(name_values)} names and saved to {csv_file_path}")
