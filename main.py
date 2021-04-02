import re
import numpy as np
import sys
from time import sleep

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
    
    # Untruncates numpy array output
    np.set_printoptions(threshold=sys.maxsize)

    # Indexed dict containing all usernames and occurences of said usernames
    indexed = {}
    # Restocks array without excess
    restockers = np.array([])
    # Choose vending/shop/both
    restock_choice = input("Shop // Vending // Turret // Both? [1/2/3/4] :: ")
     
    if restock_choice == "1" or restock_choice == "shop":
        # Sets lines_arr equal to all restock notifs in the text
        lines_arr = np.array(re.findall("\n.+ has just restocked one item in the shop!\n", txt))

        # Trims the newline and the excess text from lines_arr and moves it to restockers
        for i in range(len(lines_arr)):
            restockers = np.append(restockers, re.sub("\n", "", lines_arr[i])) 
            np.put(restockers, i, re.sub(" has just restocked one item in the shop!", "", restockers[i]))
        
        # Indexes values by restock amount
        for i in range(len(restockers)):
            if (restockers[i] in indexed) != True:
                indexed[restockers[i]] = 1
            else:
                indexed[restockers[i]] += 1
    
    if restock_choice == "2" or restock_choice == "vending":
        # Sets lines_arr equal to all restock notifs in the text
        lines_arr = np.array(re.findall("\n.+ has just restocked a vending machine!\n", txt))

        # Trims the newline and the excess text from lines_arr and moves it to restockers
        for i in range(len(lines_arr)):
            restockers = np.append(restockers, re.sub("\n", "", lines_arr[i])) 
            np.put(restockers, i, re.sub(" has just restocked a vending machine!", "", restockers[i]))
        
        # Indexes values by restock amount
        for i in range(len(restockers)):
            if (restockers[i] in indexed) != True:
                indexed[restockers[i]] = 1
            else:
                indexed[restockers[i]] += 1
    

    if restock_choice == "3" or restock_choice == "turret":
        # Sets lines_arr equal to all restock notifs in the text
        lines_arr = np.array(re.findall("\n.+ has just restocked a turret!\n", txt))

        # Trims the newline and the excess text from lines_arr and moves it to restockers
        for i in range(len(lines_arr)):
            restockers = np.append(restockers, re.sub("\n", "", lines_arr[i])) 
            np.put(restockers, i, re.sub(" has just restocked a turret!", "", restockers[i]))
        
        # Indexes values by restock amount
        for i in range(len(restockers)):
            if (restockers[i] in indexed) != True:
                indexed[restockers[i]] = 1
            else:
                indexed[restockers[i]] += 1
    # "Indexes" prints amounts of restocks, "Print" prints all names in order of occurence ... 
    # ...  "Len" prints the number of restocks in that time period
    print_choice = input("Indexes // Print // Len [1/2/3] :: ")
    
    if print_choice == "1":
        print(indexed)
    
    elif print_choice == "2":
        print(restockers)
    
    elif print_choice == "3":
        print(len(lines_arr))
   
    elif print_choice == "4":
       print("What're you trying to pull?")
    
    elif print_choice == "5":
        print("Listen man, there's nothing here for you")

    elif print_choice == "6":
        print("You're really starting to annoy me pal!")

    elif print_choice == "7":
        print("We don't have any more options! Go away!")
    
    elif print_choice == "8":
        print("That's it! I'm closing the prompt!\n.\n..\n...")
        sleep(2)
        exit()

    else:
        print("\nInvalid input\n")

except KeyboardInterrupt: 
    print("\n\nProgram stopped\n")
