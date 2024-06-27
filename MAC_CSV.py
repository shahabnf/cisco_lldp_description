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


# Regular expression to match the required patterns
pattern = re.compile(r'(.*?)(Gi\d/\d/\d+|Te\d/\d/\d+)\b\s+(\d+)\s+([A-Z,]+)\s+(\S+)')

# List to store results
results = []

# Find matches for the pattern
matches = pattern.findall(input_text)

# Add matches to results list, stripping trailing spaces from the first part
for match in matches:
    results.append((match[0].rstrip(), match[1], match[2], match[3], match[4]))
'''
# Output results
for result in results:
    print(result)
    '''

# Write results to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(['Device ID', 'Local Intf', 'Hold-time', 'Capability', 'Port ID'])
    # Write rows
    writer.writerows(results)

print("Results have been written to output.csv")