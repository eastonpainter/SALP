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

    # Untruncates numpy array output
    np.set_printoptions(threshold=sys.maxsize)

    # Indexed dict containing all usernames and occurences of said usernames
    indexed = {}
    # Restocks array without excess
    restockers = np.array([])
    # Choose vending/shop/both
    restock_choice = input("Shop // Vending // Turret // Both? [1/2/3/4] :: ")
     
    # Function to count restocks of whatever is called
    # "num", "word", and "char" are used for user input, while "text" is the restock text
    def restock_count(num, word, char, text):
        global lines_arr
        global restockers
        global indexed 
        if restock_choice == num or restock_choice == word or restock_choice == char:
            # Sets lines_arr equal to all restock notifs in the text
            lines_arr = np.array(re.findall("\n.+" + text + "\n", txt))
            # Trims the newline and the excess text from lines_arr and moves it to restockers
            for i in range(len(lines_arr)):
                restockers = np.append(restockers, re.sub("\n", "", lines_arr[i])) 
                np.put(restockers, i, re.sub(text, "", restockers[i]))
            # Indexes values by restock amount
            for i in range(len(restockers)):
                if (restockers[i] in indexed) != True:
                    indexed[restockers[i]] = 1
                else:
                    indexed[restockers[i]] += 1

    restock_count("1", "shop", "s", " has just restocked one item in the shop!")
    restock_count("2", "vending", "t", " has just restocked a vending machine!")
    restock_count("3", "turret", "t", " has just restocked a turret!")

    # "Indexes" prints amounts of restocks, "Print" prints all names in order of occurence ... 
    # ...  "Len" prints the number of restocks in that time period
    print_choice = input("Indexes // Print // Len [1/2/3] :: ")
    
    if print_choice == "1":
        print(indexed)
    
    elif print_choice == "2":
        print(restockers)
    
    elif print_choice == "3":
        print(len(lines_arr))

    else:
        print("\nInvalid input\n")

except KeyboardInterrupt: 
    print("\n\nProgram stopped\n")
