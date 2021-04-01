import re
import numpy as np
import sys

with open('restock-logs2021-03-21-to-2021-03-28.txt', 'r') as file:
    txt = file.read()

# Indexed dict containing all usernames and occurences of said usernames
indexed = {}
lines_arr_nn = np.array([])

np.set_printoptions(threshold=sys.maxsize)

lines_arr = np.array(re.findall("\n.+ has just restocked one item in the shop!\n", txt))

# lines_arr_str = ''
# for i in range(len(lines_arr)):
#     lines_arr_str += lines_arr[i]

# lines_arr_nn = re.sub("!\n", "!", lines_arr_str) 
# Traverses through unfilted array, trimming values with regexps
for i in range(len(lines_arr)):
    lines_arr_nn = np.append(lines_arr_nn, re.sub("\n", "", lines_arr[i])) 
    np.put(lines_arr_nn, i, re.sub(" has just restocked one item in the shop!", "", lines_arr_nn[i]))


#print(lines_arr_nn)

#user_list_str = re.sub(" has just restocked one item in the shop!", "", lines_arr_nn)

print(np.array2string(lines_arr_nn, separator=', '))

"""
print(lines_arr)
choice = input("Len or print [1/2] :: ")

if int(choice) == 1:
    print(len(x))

else:
    print(x)
"""
