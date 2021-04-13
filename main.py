import re
import numpy as np
import sys
# import march

# User input for log choice
# TODO: add custom .txt input
# TODO: add processing for time and repairs
# TODO: custom time input
# TODO: finish GUI
# TODO: add total restocks
# TODO: add command support

print("Note: only '4' input is supported for time")
# Try/Except statement for keyboard interrupt 
try:
    global log
    log = input("Which log? [m/f/m2/time] :: ")

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

    elif log == "timemarch" or log == "4" or log == "tm":
        with open('activity-logs-2021-02-28-to-2021-04-01.txt', 'r', encoding='utf8') as file:
            txt = file.read()

    # Untruncates numpy array output
    np.set_printoptions(threshold=sys.maxsize)
    # Indexed dict containing all usernames and occurences of said usernames
    indexed = {}
    # Restocks array without excess
    restockers = np.array([])
    active_users = np.array([])
    time_logged = np.array([])
    secs_logged = np.array([])
    
    # Choose vending/shop/both
    if log != "4": 
        restock_choice = input("Shop // Vending // Turret // All [1/2/3/4] :: ")
    # elif log != "timemarch": 
    #     restock_choice = input("Shop // Vending // Turret // All [1/2/3/4] :: ")
    # elif log != "tm": 
    #     restock_choice = input("Shop // Vending // Turret // All [1/2/3/4] :: ")
    rmsg = " has just restocked "

    # Finds maximum key of inputted dictionary and outputs it with username
    def max_key(dict1):
        max1 = list(indexed.values())[0]
        user = ''
        # What is this? Lisp
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
                print("", file=open("output.csv", "w"))
                print(str(rev_keys[i]) + "," + str(rev_vals[i]), file=open("output.csv", "a"))

        else:
            print("Invalid argument for sort_dict()")

    # Function to count restocks of whatever is called
    # "num", "word", and "char" are used for user input, while "text" is the restock text
    def restock_count(num, word, char, text):
        global lines_arr
        global restockers
        global indexed 
        global txt 
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
    
    def get_sec(time_str):
        time_str = re.sub("[hms]", "", time_str)
        h, m, s = time_str.split(':')
        return int(int(h) * 3600 + int(m) * 60 + int(s))

    # Mayusachi's Session Time: 00h:17m:51s 
    def time_spent():
        global txt
        global active_users
        global time_logged
        global secs_logged
        # Sets lines_arr equal to all lines containing session time
        lines_arr = np.array(re.findall("\n.+'s Session Time: \d{2}h:\d{2}m:\d{2}s\n", txt))
        # Creates an array with all the users who logged time in the text
        for i in range(len(lines_arr)):
            active_users = np.append(active_users, re.sub("\n", "", lines_arr[i])) 
            np.put(active_users, i, re.sub("'s Session Time.+$", "", active_users[i]))
        
        # Makes an array of all logged times in hh:mm:ss
        for i in range(len(lines_arr)):
            time_logged = np.append(time_logged, re.sub("\n", "", lines_arr[i])) 
            np.put(time_logged, i, re.sub(".+'s Session Time: ", "",  time_logged[i]))

        # Makes an array of all logged times in seconds
        for i in range(len(lines_arr)):
            secs_logged = np.append(secs_logged, get_sec(time_logged[i]))
        
        # user_times_secs = dict(zip(active_users, secs_logged))
        # print(user_times_secs)
        # user_times = dict(zip(active_users, time_logged))
        # print(user_times)
        # print("\n\n" + str(len(user_times_secs)) + "\n" + str(len(user_times)))

        # for i range(len(singles):
        #   target = singles[i]
        #   for j in range(len(dups):
        #       if dups[j] == target:
        #           singles[target] = seconds[j]

        exit()

    time_spent()
    # Restock counting functions for different types
    restock_count("1", "shop", "s", rmsg + "one item in the shop!")
    restock_count("2", "vending", "v", rmsg + "a vending machine!")
    restock_count("3", "turret", "t", rmsg + "a turret!")

    # "Indexes" prints amounts of restocks, "Print" prints all names in order of occurence ... 
    # ...  "Len" prints the number of restocks in that time period
    if log != "timemarch" or log != "4" or log != "tm": 
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
