import re
import numpy as np
import sys
    
# User input for log choice
# TODO: add custom .txt input
try:
    log = input("Which log? :: ")
    
    # March logs input
    if log == "mar" or log == "1":
        with open('restock-logs2021-03-21-to-2021-03-28.txt', 'r') as file:
            txt = file.read()
    
    # February logs input
    elif log == "feb" or log == "2":
        with open('restock-logs2021-02-14-to-2021-02-19.txt', 'r') as file:
            txt = file.read()
    
    # Indexed dict containing all usernames and occurences of said usernames
    indexed = {}
    # Restocks array without excess
    lines_arr_nn = np.array([])
    
    # Untruncates numpy array output
    np.set_printoptions(threshold=sys.maxsize)
    
    # Sets lines_arr equal to all restock notifs in the text
    lines_arr = np.array(re.findall("\n.+ has just restocked one item in the shop!\n", txt))
    
    # Trims the newline and the excess text from lines_arr and moves it to lines_arr_nn
    for i in range(len(lines_arr)):
        lines_arr_nn = np.append(lines_arr_nn, re.sub("\n", "", lines_arr[i])) 
        np.put(lines_arr_nn, i, re.sub(" has just restocked one item in the shop!", "", lines_arr_nn[i]))
    
    # Indexes values by restock amount
    for i in range(len(lines_arr_nn)):
        if (lines_arr_nn[i] in indexed) != True:
            indexed[lines_arr_nn[i]] = 1
    
        else:
            indexed[lines_arr_nn[i]] += 1
    
    # Indexes prints amounts of restocks, print prints all names in order of occurence, len prints the number of restocks in that time period
    choice = input("Indexes // Print // Len [1/2/3] :: ")
    
    if choice == "1":
        print(indexed)
    
    elif choice == "2":
        print(lines_arr_nn)
    
    elif choice == "3":
        print(len(lines_arr))
   
   elif choice == "4":
       print("What're you trying to pull?")

    else:
        print("Invalid input\n")

except KeyboardInterrupt: 
    print("\n\nProgram stopped\n")
