import re
import csv
import os
from Connection_ssh_lldp_txt_v2 import run_ssh_command as run_ssh_command
from Connection_ssh_lldp_txt_v2 import find_mac_missing_intf as find_mac_missing_intf
from Connection_ssh_lldp_txt_v2 import add_mac_to_lldp_output_text #as add_mac_to_lldp_output_text
from Connection_ssh_lldp_txt_v2 import filename1


# Find ports regex
pattern_interface = re.compile(r'Gi[^\s]*\s', re.MULTILINE)


def read_input_file(file_path):
    """Reads the input text from the specified file."""
    with open(file_path, 'r') as file:
        return file.read()

def find_matches(input_text):
    """Finds matches in the input text based on the defined pattern."""
    # Regular expression to match the required patterns, including MAC addresses (New Cisco interface pattern Gi1/0/1)
    pattern = re.compile(r'(.*?)(Gi\d/\d/\d+|Te\d/\d/\d+|[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\b\s+(\d+)\s+([A-Z,]*)\s+(\S+)')
    # Old Cisco interface pattern (Gi1/1)
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


def collect_interface(matches):
    intf_list = []
    for match in matches:
        intf_list.append(match[1].strip())
    return intf_list


def compare_intf_lldp_and_status(text1,text2):
    result = []
    for t in text1:
        if t not in text2:
            result.append(t)
    return result


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
    
    all_intf_lldp = collect_interface(matches)

    command ="show interfaces status | include connected"
    output_intf_status = run_ssh_command(command)

    # find_intf_pattern_match(output_intf_status)
    result_all_intf_status = pattern_interface.findall(output_intf_status)
    all_intf_status = [intf.strip() for intf in result_all_intf_status]

    missing_interface = compare_intf_lldp_and_status(all_intf_status, all_intf_lldp)
    print('Missing interface(s) from lldp command:', missing_interface)

    if missing_interface != []:
        extra_intf_mac = []
        for intf in missing_interface:
            extra_intf_mac +=  find_mac_missing_intf(intf)
        print("Found MAC for missing interface(s):" , extra_intf_mac)
        # Find Vendor and add to file in first field 
        add_mac_to_lldp_output_text(extra_intf_mac, (f"output-{filename1}.txt"))


    # Read the input text from the new file, Find matches for the pattern, Process matches
    input_text = read_input_file(input_file_path) 
    matches = find_matches(input_text)
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
