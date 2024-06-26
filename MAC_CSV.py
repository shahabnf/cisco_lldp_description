import csv
import re


# Input text
input_text = """Device ID           Local Intf     Hold-time  Capability      Port ID
IP Phone            Gi2/0/23       120        B,T             f8bb.1234.1234
IP Phone            Gi2/0/15       120        B,T             f8bb.1234.1234
IP Phone            Gi2/0/16       120        B,T             f8bb.1234.1234
IP Phone            Gi1/0/10       120        B,T             f8bb.1234.1234
AccessPoint_02      Gi4/0/5        120        B               Gi0
AccessPoint_07      Gi4/0/7        120        B               Gi0
AccessPoint_06      Gi1/0/17       120        B               Gi0
AP_05		    Gi1/0/23       120        B               Gi0
IP Phone            Gi3/0/20       120        B,T             f8bb.1234.1234
AP_HP	            Gi4/0/10       120        B               Gi0
AP_New_AP_newVeryNewGi4/0/8        120        B               Gi0
ANewSwitch.NewSwitchTe1/1/1        120        B,R             Gi3/0/2"""


# Create a list to store rows for CSV
csv_data = []

# Split input text into lines
lines = input_text.split('\n')

# Iterate over each line
for line in lines[1:]:  # Skip the header line
    # Split line into cells
    match_Gi_Te = re.search(r'(Gi|Te)(\d/\d)', line[0])
    # match2 = re.search(r'(\ddd+)', line[0])
    cells = line.split()

    # Check if the second cell starts with "Gi", "Te1", "Te2", "Te3", or "Te4"
    if cells[1].startswith(("Gi", "Te1", "Te2", "Te3", "Te4")):
        # Combine the first and second cells
        new_cells = [cells[0] ] + cells[1:]
        # new_cells = [cells[0] + "," + cells[1]] + cells[2:]
        
    elif cells[2].startswith(("Gi", "Te1", "Te2", "Te3", "Te4")):
        new_cells = [cells[0] + " " + cells[1] ] + cells[2:]
        # new_cells = [cells[0] + " " + cells[1] + "," + cells[2] ] + cells[3:]

    elif cells[3].startswith(("Gi", "Te1", "Te2", "Te3", "Te4")):
        new_cells = [cells[0] + " " + cells[1] + " " + cells[2] ] + cells[3:]
        # new_cells = [cells[0] + " " + cells[1] + " " + cells[2] + "," + cells[3]  ] + cells[4:]
    # elif cells[0].find("Gi"):
    # elif match_Gi_Te: 
    #        
    elif re.search(r'(Gi|Te)(\d/)', cell[0]): 
        print(cell[0])      
        index_te1 = input_text.find("Te1")
        # Separate the text into two parts
        before_te1 = input_text[:index_te1]
        after_te1 = input_text[index_te1:]
        new_cells = [before_te1, after_te1]
    
    else:
        new_cells = cells
    
    # Append the modified cells to the CSV data list
    # csv_data.append(new_cells)
    print(new_cells)

# Write CSV file
csv_file_path = 'output.csv'
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(csv_data)

print(f"CSV file saved at: {csv_file_path}")
