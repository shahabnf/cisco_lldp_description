# Cisco LLDP Description

This script will find the Cisco interface(s) and the associated connected MAC address(es) using the "Show LLDP neighbors" command.

The result/output of "show lldp neighbors" will be sorted alphabetically by Gigabit and TenGigabit and stored in a CSV file.

The "show power inline" command will find the CCTV camera(s) connected to the switch and the result will be added to the end of the csv file.

Next, the script perform "show interfaces status" and find all the connected interfaces and compare it with the result of lldp command, if there is a missing interface(s) the interface and MAC address will be added to output text file.

Then, the script will create a description for each connected interface to assist network admins with adding descriptions to interfaces.

At the end of the script, all the output-generated files will be moved to the "output" directory for easier access.

# File structure
The files starting with capital letters are modules with various functions.


# Package Dependencies: 
Package dependencies are located in the requirement file.

```
    pip install -r requirements.txt
```

# Run the script
Navigate to the script path. Execute the following command to start the script. Find the result(s) in "output" directory.

```
    python .\cisco_switch_description_generator.py
```