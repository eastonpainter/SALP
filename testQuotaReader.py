# Importing modules
import re
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

# <<<Functions>>>

def sort_dict(dict1):
    sorted_dict = {}
    sorted_keys = sorted(dict1, key=dict1.get)
    print(sorted_keys)

    for i in sorted_keys:
       sorted_dict[i] = dict1[i]

    return sorted_dict

def pretty_print(dict1):
    sorted_dict = sort_dict(dict1)
    keys = list(dict1.keys())
    vals = list(dict1.values())
    max_len = len(keys[0])

    for j in range(len(sorted_dict)):
        if len(keys[j]) > max_len:
            max_len = len(keys[j])
            
    for i in range(len(sorted_dict)):
        spaces = int((max_len - len(keys[i])) + 6) * " "        
        print(str(keys[i]) + spaces + str(vals[i]))

# Variables
en = 'utf8'
rawData = open('RawData.txt', 'r', encoding=en)
indexed = {}

# <<<Shop restocks>>>
text = ".+ has just restocked one item in the shop!"
with open('RawData.txt', 'r', encoding=en) as file:
    rawData = file.read()

searchedText = re.findall(text, rawData)
restockers = np.array([])

for i in range(len(searchedText)):
    subbed_line = re.sub(" has just restocked one item in the shop!", "", searchedText[i])
    restockers = np.append(restockers, subbed_line)  

for i in range(len(restockers)):
    if restockers[i] not in indexed:
        indexed[restockers[i]] = 1
    else:
        indexed[restockers[i]] += 1

# <<<Program end>>>
pretty = input("Pretty? [Y/N] :: ")
if pretty == "n" or pretty == "N":
    print(indexed)
elif pretty == "y" or pretty == "Y":
    print(pretty_print(indexed))
else:
    print("Invalid input :/")
