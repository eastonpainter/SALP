import re

with open('restock-logs2021-03-21-to-2021-03-28.txt', 'r') as file:
    txt = file.read()

lines_arr = re.findall("\n.+ has just restocked one item in the shop!\n", txt)

lines_arr_str = ''
for i in range(len(lines_arr)):
    lines_arr_str += lines_arr[i]

lines_arr_nn = re.sub("!\n", "!", lines_arr_str) 

#print(lines_arr_nn)

user_list_str = re.sub(" has just restocked one item in the shop!", "", lines_arr_nn)

print(user_list_str)

"""
print(lines_arr)
choice = input("Len or print [1/2] :: ")

if int(choice) == 1:
    print(len(x))

else:
    print(x)
"""
