import re
import csv
import os


def read_input_file(file_path):
    """Reads the input text from the specified file."""
    with open(file_path, 'r') as file:
        return file.read()

def find_matches(input_text):
    """Finds matches in the input text based on the defined pattern."""
    # Regular expression to match the required patterns, including MAC addresses (New pattern Gi1/0/1)
    pattern = re.compile(r'(.*?)(Gi\d/\d/\d+|Te\d/\d/\d+|[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\b\s+(\d+)\s+([A-Z,]*)\s+(\S+)')
    # Old pattern (Gi1/1)
    if pattern.findall(input_text) == []:
        pattern = re.compile(r'(.*?)(Gi\d/\d+|Te\d/\d+|[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\b\s+(\d+)\s+([A-Z,]*)\s+(\S+)')
    return pattern.findall(input_text)

def process_matches(matches):
    """Processes the matches to strip trailing spaces from the first part and store them in a list."""
    results = []
    for match in matches:
        results.append((match[0].rstrip(), match[1], match[2], match[3], match[4]))
    return results

def sort_by_local_intf(results):
    """Sorts the results based on the Local Intf field alphabetically."""
    return sorted(results, key=lambda x: x[1])

def write_to_csv(results, output_file_path):
    """Writes the processed results to a CSV file."""
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Device ID', 'Local Intf', 'Hold-time', 'Capability', 'Port ID'])
        # Write rows
        writer.writerows(results)

def main():
    # Define the input and output file paths
    input_file_path = os.path.join(os.getcwd(), 'output-lldp.txt')
    output_file_path = os.path.join(os.getcwd(), 'output-lldp-compiled.csv')
    
    # Read the input text from the file
    input_text = read_input_file(input_file_path)
    
    # Find matches for the pattern
    matches = find_matches(input_text)
    
    # Process matches to strip trailing spaces
    results = process_matches(matches)
    
    # Sort results by Local Intf alphabetically
    sorted_results = sort_by_local_intf(results)
    
    # Write results to a CSV file
    write_to_csv(sorted_results, output_file_path)
    
    # Print confirmation message
    print(f"Results have been written to ---> {output_file_path}")

# Execute the main function
if __name__ == '__main__':
    main()
