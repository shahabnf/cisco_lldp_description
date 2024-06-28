import csv
import re
import os


# Set values
# Get the current directory
current_directory = os.getcwd()
input_file_path = os.path.join(current_directory, 'lldp-sample.txt')


# Read the input text file
with open(input_file_path, 'r') as input_file:
    input_text_lines = input_file.read()


# Regular expression to match the required patterns
pattern = re.compile(r'(.*?)(Gi\d/\d/\d+|Te\d/\d/\d+)\b\s+(\d+)\s+([A-Z,]+)\s+(\S+)')

# Empty List to store results
results = []

# Find matches for the pattern
matches = pattern.findall(input_text_lines)

# Add matches to results list, stripping trailing spaces from the first part
for match in matches:
    results.append((match[0].rstrip(), match[1], match[2], match[3], match[4]))


# Get the current directory
current_directory = os.getcwd()
output_file_path = os.path.join(current_directory, 'output.csv')


# Write results to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(['Device ID', 'Local Intf', 'Hold-time', 'Capability', 'Port ID'])
    # Write rows
    writer.writerows(results)

# print("Results have been written to output.csv")
print(f"Results have been written to ---> {output_file_path}")