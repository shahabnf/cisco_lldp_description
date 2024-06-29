import csv
import os
from collections import defaultdict


def read_csv_file(file_path):
    """Reads the CSV file and returns the rows."""
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header
        return [row for row in reader]

def write_to_new_file(rows, output_file_path):
    """Writes the processed rows to a new file."""
    # Dictionary to collect entries by "Local Intf"
    local_intf_dict = defaultdict(list)

    # Populate the dictionary
    for row in rows:
        local_intf_dict[row[1]].append(row)

    # Write the processed data to the output file
    with open(output_file_path, 'w') as file:
        for local_intf, entries in local_intf_dict.items():
            if len(entries) == 1 and "IP Phone" in entries[0][0]:
                # Single entry with "IP Phone"
                file.write(f"interface {entries[0][1]}\n")
                file.write(f"description Phone-{entries[0][4]}\n\n")
            elif len(entries) == 2:
                # Two entries with the same "Local Intf"
                device_ids = [entry[0] for entry in entries]
                if "IP Phone" in device_ids:
                    ip_phone_entry = entries[device_ids.index("IP Phone")]
                    other_entry = entries[1 - device_ids.index("IP Phone")]
                    file.write(f"interface {local_intf}\n")
                    file.write(f"description Phone-{ip_phone_entry[4]}-WS-{other_entry[4]}\n\n")

def main():
    # Define the input and output file paths
    input_file_path = os.path.join(os.getcwd(), 'output.csv')
    output_file_path = os.path.join(os.getcwd(), 'result.txt')
    
    # Read the CSV file
    rows = read_csv_file(input_file_path)
    
    # Write to the new file
    write_to_new_file(rows, output_file_path)
    
    # Print confirmation message
    print(f"Processed results have been written to ---> {output_file_path}")

# Execute the main function
if __name__ == '__main__':
    main()
