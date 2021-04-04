import re
import numpy as np
import sys
# import march

# User input for log choice
# TODO: add custom .txt input
# TODO: add command support

# Try/Except statement for keyboard interrupt 
try:
    log = input("Which log? [m/f/m2] :: ")

    # March logs input
    if log == "mar" or log == "1" or log == "m1":
        with open('restock-logs2021-03-21-to-2021-03-28.txt', 'r', encoding='utf8') as file:
            txt = file.read()

    # February logs input
    elif log == "feb" or log == "2" or log == "f":
        with open('restock-logs2021-02-14-to-2021-02-19.txt', 'r', encoding='utf8') as file:
            txt = file.read()

    # Complete March logs input
    elif log == "mar2" or log == "3" or log == "m2":
        with open('restock-logs2021-02-28-to-2021-04-01.txt', 'r', encoding='utf8') as file:
                txt = file.read()

    # Untruncates numpy array output
    np.set_printoptions(threshold=sys.maxsize)
    # Indexed dict containing all usernames and occurences of said usernames
    indexed = {}
    # Restocks array without excess
    restockers = np.array([])
    # Choose vending/shop/both
    restock_choice = input("Shop // Vending // Turret // All [1/2/3/4] :: ")
    rmsg = " has just restocked "

    # Finds maximum key of inputted dictionary and outputs it with username
    def max_key(dict1):
        max1 = list(indexed.values())[0]
        user = ''
        for i in range(len(list(dict1.values()))):
            if list(dict1.values())[i] > max1:
                max1 = list(dict1.values())[i]
                user = list(dict1)[i]

        print(user + " ::  " + str(max1))

    def sort_dict(indexes, pretty):
        dict_len = len(indexes)
        # Sorts the dict by value in least to greatest
        sorted_dict = {}
        sorted_keys = sorted(indexes, key=indexes.get)

        for w in sorted_keys:
            sorted_dict[w] = indexes[w]

        # Creates two separate sorted arrays for the values and keys 
        rev_vals = list(reversed(list(sorted_dict.values())))
        rev_keys = list(reversed(list(sorted_dict.keys())))

        # Zips the two sorted arrays
        final = dict(zip(rev_keys, rev_vals))
        
        if pretty == 'n':
            print(final)

        elif pretty == 'y':
            for i in range(dict_len):
                print(str(i+1) + ". " + str(rev_keys[i]) + " ::: " + str(rev_vals[i]))

        elif pretty == 'd':
            print(indexes)

        elif pretty == 'csv':
            for i in range(dict_len):
                print(str(rev_keys[i]) + "," + str(rev_vals[i]), file=open("output.csv", "w"))

        else:
            print("Invalid argument for sort_dict()")

    # Function to count restocks of whatever is called
    # "num", "word", and "char" are used for user input, while "text" is the restock text
    def restock_count(num, word, char, text):
        global lines_arr
        global restockers
        global indexed 
        if restock_choice == num or restock_choice == word or restock_choice == char or restock_choice == "4":
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

    # Restock counting functions for different types
    restock_count("1", "shop", "s", rmsg + "one item in the shop!")
    restock_count("2", "vending", "v", rmsg + "a vending machine!")
    restock_count("3", "turret", "t", rmsg + "a turret!")

    # "Indexes" prints amounts of restocks, "Print" prints all names in order of occurence ... 
    # ...  "Len" prints the number of restocks in that time period
    print_choice = input("Indexes // Print // Len // Max [1/2/3/4] :: ")

    if print_choice == "1":
        pretty = input("Pretty? [y/n/d/csv] :: ")
        if pretty == 'y':
            sort_dict(indexed, pretty)
        elif pretty == 'n':
            sort_dict(indexed, pretty)
        elif pretty == 'd':
            sort_dict(indexed, pretty)
        elif pretty == 'csv':
            sort_dict(indexed, pretty)

    elif print_choice == "2":
        print(restockers)
    
    elif print_choice == "3":
        print(len(restockers))

    elif print_choice == "4":
        max_key(indexed)

    else:
        print("\nInvalid input\n")

except KeyboardInterrupt: 
    print("\n\nProgram stopped\n")
