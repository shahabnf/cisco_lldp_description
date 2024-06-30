import csv
import os
import re
from collections import defaultdict


def read_csv_file(file_path):
    """Reads the CSV file and returns the rows."""
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header
        return [row for row in reader]


def find_mac_address(file_path):
    """Finds the first MAC address matching the pattern in the specified file."""
    pattern = re.compile(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})')
    
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                return match.group(1)
    return None
    


def write_to_new_file(rows, mac_file_path, output_file_path):
    """Writes the processed rows to a new file."""
    # Dictionary to collect entries by "Local Intf"
    local_intf_dict = defaultdict(list)

    # Populate the dictionary
    for row in rows:
        local_intf_dict[row[1]].append(row)

    # Write the processed data to the output file
    with open(output_file_path, 'w') as file:
        for local_intf, entries in local_intf_dict.items():
            
            # Find signle IP Phone on the port
            if len(entries) == 1 and "IP Phone" in entries[0][0]:
                # Single entry with "IP Phone"
                file.write(f"interface {entries[0][1]}\n")
                file.write(f"description Phone-{entries[0][4]}\n\n")
            
            # Find IP Phone and Workstation on same port
            elif len(entries) == 2:
                # Two entries with the same "Local Intf"
                device_ids = [entry[0] for entry in entries]
                if "IP Phone" in device_ids:
                    ip_phone_entry = entries[device_ids.index("IP Phone")]
                    other_entry = entries[1 - device_ids.index("IP Phone")]
                    file.write(f"interface {local_intf}\n")
                    file.write(f"description Phone-{ip_phone_entry[4]}-WS-{other_entry[4]}\n\n")
            
            # Find Access Point without MAC address 
            elif len(entries) == 1 and "120" in entries[0][2] and "Gi0" in entries[0][4]:
                mac_address = find_mac_address(mac_file_path)               
                if mac_address:
                    file.write(f"interface {entries[0][1]}\n")
                    file.write(f"description {entries[0][0]}-{mac_address}\n\n")


def main():
    # Define the input and output file paths
    input_file_path = os.path.join(os.getcwd(), 'output.csv')
    output_file_path = os.path.join(os.getcwd(), 'result.txt')
    mac_file_path = os.path.join(os.getcwd(), 'lldp-sho-mac-add.txt')
    
    # Read the CSV file
    rows = read_csv_file(input_file_path)
    
    # Write to the new file
    write_to_new_file(rows, mac_file_path, output_file_path)
    
    # Print confirmation message
    print(f"Processed results have been written to ---> {output_file_path}")

# Execute the main function
if __name__ == '__main__':
    main()
