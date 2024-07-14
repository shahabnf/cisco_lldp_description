import paramiko
import getpass
import re
import csv


ip = None
username = None
password = None


# Find ports regex
pattern_interface = re.compile(r'Gi[^\s]*\s', re.MULTILINE)
pattern_mac = pattern = re.compile(r'([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+DYNAMIC\s+(Gi[^\s]*)', re.IGNORECASE)



# Commands list
command1, filename1 = "show lldp neighbors", "lldp"
command2, filename2 = "show power inline | inc 7.0|15.4",""
command3, filename3 = "show mac address interface ", ""

def read_input_file(file_path):
    """Reads the input text from the specified file."""
    with open(file_path, 'r') as file:
        return file.read()


def find_matches_interface(pattern, input_text):
    """Finds matches in the input text based on the defined pattern."""
    matches = pattern.findall(input_text)
    cleaned_matches = [match.strip() for match in matches]
    print("Found CCTV camera(s) with 'show power inline' command in these port(s):",cleaned_matches)
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
    return mac[0][0]

def get_switch_details():
    """Prompt the user for switch connection details."""
    global ip
    global username
    global password
    ip = input("Enter switch IP: ")
    username = input("Enter username: ")
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
    
    # Connect to switch and run the show lldp neighbours
    connect_to_switch_and_run_command(ip, username, password, command1, filename1, pattern_interface)
    
    # Connect to switch and run the show power inline  
    ports = connect_to_switch_and_run_command(ip, username, password, command2, filename2, pattern_interface)
    
    # if the result of power inline was not empty
    if ports != []:
        mac_int = ""
        for port in ports:
            command = command3 + port 
            mac_int += connect_to_switch_and_run_command(ip, username, password, command , filename3, pattern_mac)
        
        
        # Read the output of command 3 and find all the maches in text
        mac_matches = []
        mac_matches = find_matches_mac(pattern_mac, mac_int)
    
        # Add the result of MACs and ports to the text file 
        add_mac_to_lldp_output_text(mac_matches,(f"output-{filename1}.txt"))



if __name__ == "__main__":
    main()
