import paramiko
import getpass
import re
import csv
# import Find_MAC_CSV
# import Description_generator


ip = None
username = None
password = None


# Find ports regex
pattern_interface = re.compile(r'Gi[^\s]*\s', re.MULTILINE)
pattern_mac = pattern = re.compile(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+DYNAMIC\s+(Gi[^\s]*)', re.IGNORECASE)
# pattern_mac = re.compile(r'(.*?)([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\b\s', re.MULTILINE)
# pattern_mac = re.compile(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})', re.IGNORECASE)
# pattern_mac = pattern = re.compile(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+DYNAMIC\s+(Gi\d+/\d+)', re.IGNORECASE)



# commands = [("show lldp neighbors", "lldp"),("show power inline | inc 7.0|15.4","power-inline")]
command1, filename1 = "show lldp neighbors", "lldp"
command2, filename2 = "show power inline | inc 7.0|15.4",""
# command3, filename3 = "show mac address interface ", "power-mac"
command3, filename3 = "show mac address interface ", ""

def read_input_file(file_path):
    """Reads the input text from the specified file."""
    with open(file_path, 'r') as file:
        return file.read()


def find_matches_interface(pattern, input_text):
    """Finds matches in the input text based on the defined pattern."""
    matches = pattern.findall(input_text)
    cleaned_matches = [match.strip() for match in matches]
    print("Found MAC pattern in these ports",cleaned_matches)
    return cleaned_matches


def find_matches_mac(pattern, input_text):
    """Finds matches in the input text based on the defined pattern."""
    matches = pattern.findall(input_text)
    
    if type(matches[0]) == tuple:
        cleaned_matches = [(mac.strip(), intf.strip()) for mac, intf in matches]
    else:
        cleaned_matches = [match.strip() for match in matches]

    return cleaned_matches

def find_mac_address(interface):
    command = f"show mac add int {interface}"
    # ip, username, password = get_switch_details()
    filename=""
    output = connect_to_switch_and_run_command(ip, username, password, command, filename, pattern_mac)
    mac = find_matches_mac(pattern_mac, output)
    # print("Found this tuple",mac, "found this MAC", mac[0][0])
    return mac[0][0]

def get_switch_details():
    """Prompt the user for switch connection details."""
    # ip = "10.16.2.19"
    # ip = "10.13.2.16"
    global ip
    global username
    global password
    ip = "10.13.2.1"
    username = "eb88"
    # ip = input("Enter switch IP: ")
    # username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    return ip, username, password


def connect_to_switch_and_run_command(ip, username, password, command, filename, pattern):
    """Connect to the switch, run commands, and save the outputs to files."""
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the switch
        ssh.connect(ip, username=username, password=password)
        
        # Run Command 
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        
        if filename != "":
            # Save the output of command 1 to a file
            with open(f"output-{filename}.txt", "a") as file:
                file.write(output)
            print(f"The outputs have been saved to output-{filename}.txt")
        elif pattern == pattern_mac:
            return output
        else:
            # print(output)
            matches = find_matches_interface(pattern, output)
            return matches

        
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the connection
        ssh.close()


def add_mac_to_lldp_output_text(input_tuples, inputfile):

    output_lines = []
    
    for mac, intf in input_tuples:
        
        # Format the line according to the specified pattern
        line = f"axis-{mac}\t{intf}\t   120\t\tS\t\t{mac}"
        output_lines.append(line)

    # Append the formatted lines to the file
    with open(inputfile, 'a') as file:
        for line in output_lines:
            file.write(line + '\n')

    
def main():
    
    ip, username, password = get_switch_details()
    
    # connect to switch and run the Show lldp neighbours
    connect_to_switch_and_run_command(ip, username, password, command1, filename1, pattern_interface)
    
    # find the result of show power inline command 
    ports = connect_to_switch_and_run_command(ip, username, password, command2, filename2, pattern_interface)
    
    # if the result of power inline was not empty
    if ports != []:
        mac_int = ""
        for port in ports:
            command = command3 + port 
            # print(command)
            mac_int += connect_to_switch_and_run_command(ip, username, password, command , filename3, pattern_mac)
        
        
        # read file -> find mac -> print mac
        # mac_filename_content = read_input_file(f"output-{filename3}.txt")
        # mac_matches = find_matches_mac(pattern_mac, mac_filename_content)
        
        # Read the output of command 3 and find all the maches in text
        mac_matches = []
        mac_matches = find_matches_mac(pattern_mac, mac_int)
    
        # Add the result of MACs and ports to the text file 
        add_mac_to_lldp_output_text(mac_matches,(f"output-{filename1}.txt"))

    # Find_MAC_CSV.main()
    # Description_generator.main()


if __name__ == "__main__":
    main()
