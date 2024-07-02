import csv
import os
import re
from collections import defaultdict
import requests


# MAC Address regex pattern
pattern = re.compile(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})')

# Vendors list as workstation
vendor_list = ["HP", "Dell", "Hewlett-Packard", "Hewlett Packard", 'Intel']

Tengig_start = True

def read_csv_file(file_path):
    """Reads the CSV file and returns the rows."""
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header
        return [row for row in reader]


def append_to_file(file_path, text):
    """Appends the given text to the end of the specified file."""
    with open(file_path, 'a') as file:
        file.write(text + '\n')


def find_mac_address(file_path):
    """Finds the first MAC address matching the pattern in the specified file."""
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                return match.group(1)
    return None
    

def get_mac_vendor_online(mac_address):
    """Queries the MAC Vendors API to get the vendor for a given MAC address."""
    url = f"https://api.macvendors.com/{mac_address}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return False
    except Exception as e:
        return str(e)


def check_mac_in_file(mac_address, file_path):
    """Checks if the first 7 characters of the given MAC address are in the All-MAC file."""
    # Normalize the MAC address to the first 7 characters
    mac_prefix = mac_address[:7].lower()

    with open(file_path, 'r') as file:
        for line in file:
            # Remove any whitespace and normalize the line to lowercase
            prefix = line.strip().lower()
            if mac_prefix == prefix:
                return True
    return False


def write_to_csv(results, output_file_path):
    """Writes the processed results to a CSV file."""
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Port', 'New Description', 'Old Description'])
        # Write rows
        writer.writerows(results)


def write_to_new_file(rows, mac_file_path, output_file_path, mac_file_path_finder, output_file_path_description_csv, Tengig_start):
    """Writes the processed rows to a new file."""
    # Dictionary to collect entries by "Local Intf"
    local_intf_dict = defaultdict(list)

    # Populate the dictionary
    for row in rows:
        local_intf_dict[row[1]].append(row)

    new_descriptions = []

    # Write the processed data to the output file
    with open(output_file_path, 'w') as file:
        for local_intf, entries in local_intf_dict.items():
            
            # Find signle IP Phone on the port
            if len(entries) == 1 and "IP Phone" in entries[0][0]:
                # Single entry with "IP Phone"
                file.write(f"interface {entries[0][1]}\n")
                file.write(f"description Phone-{entries[0][4]}\n\n")
                # Append to csv file
                new_description = [f"interface {entries[0][1]}", f"description Phone-{entries[0][4]}", ""]
                new_descriptions.append(new_description)

            # Find IP Phone and Workstation on same port
            elif len(entries) == 2 and "120" in entries[0][2] and "3601" in entries[1][2] and "B,T" in entries[0][3] :
                    file.write(f"interface {local_intf}\n")
                    file.write(f"description Phone-{entries[0][4]}-WS-{entries[1][4]}\n\n")
                    # Append to csv file
                    new_description = [f"interface {local_intf}", f"description Phone-{entries[0][4]}-WS-{entries[1][4]}", ""]
                    new_descriptions.append(new_description)

            # Find Access Point without MAC address 
            elif len(entries) == 1 and "120" in entries[0][2] and "Gi0" in entries[0][4]:
                mac_address = find_mac_address(mac_file_path)               
                if mac_address:
                    file.write(f"interface {entries[0][1]}\n")
                    file.write(f"description {entries[0][0]}-{mac_address}\n\n")
                    # Append to csv file
                    new_description = [f"interface {entries[0][1]}" , f"description {entries[0][0]}-{mac_address}", ""]
                    new_descriptions.append(new_description)

            # Find computer name with MAC address 
            elif len(entries) == 1 and "3601" in entries[0][2] and entries[0][0] != entries[0][4]:
                    file.write(f"interface {entries[0][1]}\n")
                    file.write(f"description {entries[0][0]}-{entries[0][4]}\n\n")
                    # Append to csv file
                    new_description = [f"interface {entries[0][1]}", f"description {entries[0][0]}-{entries[0][4]}", ""]
                    new_descriptions.append(new_description)

            # Find MAC Address 
            elif pattern.match(entries[0][0]) and len(entries) == 1 :
                mac_address = entries[0][0]

                # Offline MAC Address finder from file
                if check_mac_in_file(mac_address, mac_file_path_finder):
                    file.write(f"interface {entries[0][1]}\n")
                    file.write(f"description WS-{mac_address}\n\n")
                    # Append to csv file
                    new_description = [f"interface {entries[0][1]}", f"description WS-{mac_address}", ""]
                    new_descriptions.append(new_description)

                # Online MAC Address finder via API
                elif (vendor := get_mac_vendor_online(mac_address)) is not False:
                    if any(item in vendor for item in vendor_list):
                        file.write(f"interface {entries[0][1]}\n")
                        file.write(f"description WS-{mac_address}\n\n")
                        # Append to csv file
                        new_description = [f"interface {entries[0][1]}", f"description WS-{mac_address}", ""]
                        new_descriptions.append(new_description)
                        # Append to All-MAC.txt offline MAC address search
                        mac_prefix = mac_address[:7].lower()
                        append_to_file(mac_file_path_finder, mac_prefix)
                    print(f"The MAC address {mac_address} from vendor {vendor} was added to '{mac_file_path_finder}' "
                        "file for future reference as Workstation.\n")
                
                else:
                    print(f"The MAC address {mac_address} on {entries[0][1]} could not be found. Try other methods to find the vendor.\n")
            
            elif len(entries) == 1 and "B,R" in entries[0][3] :
                if Tengig_start: file.write("\n"); new_descriptions.append(["","",""]); Tengig_start = False
                # Remove all chars after dot
                device_name = entries[0][0].split('.')[0]
                file.write(f"interface {entries[0][1]}\n")
                file.write(f"description Connected to {device_name} port {entries[0][4]}\n\n")
                # Append to csv file
                new_description = [f"interface {entries[0][1]}", f"description Connected to {device_name} port {entries[0][4]}", ""]
                new_descriptions.append(new_description)

            write_to_csv(new_descriptions, output_file_path_description_csv)


def main():
    # Define the input and output file paths
    input_file_path = os.path.join(os.getcwd(), 'output.csv')
    output_file_path = os.path.join(os.getcwd(), 'result.txt')
    mac_file_path = os.path.join(os.getcwd(), 'lldp-sho-mac-add.txt')
    mac_file_path_finder = os.path.join(os.getcwd(), 'All-MAC.txt')
    output_file_path_description_csv = os.path.join(os.getcwd(), 'description-comparison.csv')
    
    # Read the CSV file
    rows = read_csv_file(input_file_path)
    
    # Write to the new file
    write_to_new_file(rows, mac_file_path, output_file_path, mac_file_path_finder, output_file_path_description_csv, Tengig_start)
    
    # Print confirmation message
    print(f"Processed results have been written to ---> {output_file_path}")

# Execute the main function
if __name__ == '__main__':
    main()
