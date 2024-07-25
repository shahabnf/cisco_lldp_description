import re
import csv
import os
from Connection_ssh_lldp_txt_v2 import run_ssh_command


def get_interfaces(csv_file_path):
    """Reads a CSV file and returns a list of interfaces from the first column without the 'interface' prefix."""
    interfaces = []
    try:
        with open(csv_file_path, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                if row:  # Ensure the row is not empty
                    interface = row[0].strip()
                    if interface.startswith("interface "):
                        interface = interface.replace("interface ", "")
                    # interfaces.append(interface)
                    if interface:  # Ensure the interface is not empty after stripping
                        interfaces.append(interface)

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return interfaces    


def parse_interface_description(text):
    """
    Parse interface descriptions from the given text.
    Args:
        text (str): The input text containing interface descriptions.
    Returns:
        List[Tuple[str, str]]: A list of tuples where each tuple contains the interface name and its description.
    """
    lines = text.strip().split('\n')
    result = []
    
    for line in lines:
        # Match interface names starting with Gi or Te
        match = re.match(r'^(Gi[1-9][0-9/]*|Te[1-9][0-9/]*)\s+up\s+up\s+(.*)$', line)
        if match:
            interface = match.group(1)
            description = match.group(2).strip()
            result.append((interface, description))
        else:
            # Check if the line matches the required interface pattern but has no description
            match_no_desc = re.match(r'^(Gi[1-9][0-9/]*|Te[1-9][0-9/]*)\s+up\s+up\s*$', line)
            if match_no_desc:
                interface = match_no_desc.group(1)
                result.append((interface, ""))
    
    return result


def update_csv_with_descriptions(tuple_list, interface_list, csv_file_path):
    """Updates the CSV file with descriptions from the tuple list based on interface matches from the interface list."""
    # Read existing CSV data
    with open(csv_file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
    
    # Create a dictionary from the tuple list for quick lookup
    description_dict = {interface: description for interface, description in tuple_list}
    
    # Update rows with descriptions
    updated_rows = []
    for row in rows:
        if len(row) > 0:  # Ensure the row is not empty
            interface = row[0].replace("interface ", "").strip()
            if interface in description_dict:
                if len(row) > 2:
                    row[2] = description_dict[interface]  # Update existing description
                else:
                    row.append(description_dict[interface])  # Add new description
        updated_rows.append(row)
    
    # Write updated rows back to the CSV file
    with open(csv_file_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updated_rows)


def main():
    command = "show interfaces description | include up"
    description_output = run_ssh_command(command)
    # print(description_output)
    output_value = parse_interface_description(description_output)

    # Add output to the path directory
    files = os.path.join(os.getcwd(), "output")
    output_file_path_description_csv = os.path.join(files, 'output_description-comparison.csv')
    
    # List intefaces in output_description_compare
    interfaces_list = get_interfaces(output_file_path_description_csv)

    # Update the csv file with new values for comparison
    update_csv_with_descriptions(output_value, interfaces_list, output_file_path_description_csv)


# Execute the main function
if __name__ == '__main__':
    main()