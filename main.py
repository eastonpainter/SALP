import re
import numpy as np
import sys
import datetime
# import march

# User input for log choice
# TODO: add custom .txt input
# TODO: add processing for time and repairs
# TODO: custom time input
# TODO: finish GUI
# TODO: add total restocks
# TODO: add command support
# TODO: organize ++ improve functions

# Untruncates numpy array output
np.set_printoptions(threshold=sys.maxsize)

welcome = """
*
**
***
****
*****
Welcome to...
     ____    _    _     ____
    / ___|  / \  | |   |  _ \\
    \___ \ / _ \ | |   | |_) |
     ___) / ___ \| |___|  __/
    |____/_/   \_\_____|_|
< ---------------------------------- >
"""

bolds = '\033[1m'
bolde = '\033[0m'
log = ""

# Indexed dict containing all usernames and occurences of said usernames
indexed = {}

# List of restocks
restockers = np.array([])

# Logged time arrays for users, time, and time in seconds
active_users = np.array([])
time_logged = np.array([])
secs_logged = np.array([])

# Startup message
def startup():
    print(welcome)

# Which file the user will read
def options_print():
    print("\nWhich log would you like to open? ")
    print("------------------------------------------------------------")
    print("     {}Month         Type            Time          Date{}       ".format(bolds, bolde))
    print("1    March         Restock         1 week        3/21 - 2/28")
    print("2    February      Restock         5 days        2/14 - 2/19")
    print("3    March         Restock         1 month       2/28 - 4/01")
    print("4    March         Activity        1 month       2/28 - 4/01")
    print("\nC-- custom     H-- help")

def file_picker(log):
    # User input to choose the log
    log = input("[1/2/3/4/c/h] >>> ")

    # Encoding type for the file opens, utf8 for compatability
    en = 'utf8'

    # March logs input
    if log == "mar" or log == "1" or log == "m1":
        with open('restock-logs2021-03-21-to-2021-03-28.txt', 'r', encoding=en) as file:
            txt = file.read()

    # February logs input
    elif log == "2":
        with open('restock-logs2021-02-14-to-2021-02-19.txt', 'r', encoding=en) as file:
            txt = file.read()

    # Complete March logs input
    elif log == "3":
        with open('restock-logs2021-02-28-to-2021-04-01.txt', 'r', encoding=en) as file:
            txt = file.read()

    # Complete March time logs
    elif log == "4":
        with open('activity-logs-2021-02-28-to-2021-04-01.txt', 'r', encoding=en) as file:
            txt = file.read()

    # Custom file selection
    elif log == "c":
        file_choice = input("\nEnter file name :: ")
        with open(file_choice, 'r', encoding=en) as file:
            txt = file.read()

    # Print help message
    elif log == "h":
        options_print()
        file_picker(log)

    # Incorrect input
    else:
        print("Not a valid log input :/")

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
    # Length of inputted dictionary for iteration
    dict_len = len(indexes)
    # Final dictionary for all sorted values
    sorted_dict = {}
    # Sorts the keys by their value
    sorted_keys = sorted(indexes, key=indexes.get)

    # Sorts the keys by their value, then put the values to their keys
    # Sets each value and key equal to the keys of the indexes
    for i in sorted_keys:
        sorted_dict[i] = indexes[i]

    # Creates two separate sorted arrays for the values and keys 
    rev_vals = list(reversed(list(sorted_dict.values())))
    rev_keys = list(reversed(list(sorted_dict.keys())))

    # Zips the two sorted arrays
    final = dict(zip(rev_keys, rev_vals))
    
    if pretty == 'n':
        print(final)

    elif pretty == 'y':
        # Pos if adds a zero to non-three-digit numbers
        for i in range(dict_len):
            if i+1 < 10:
                pos = "00" + str(i+1)
            elif i+1 < 100:
                pos = "0" + str(i+1)
            else:
                pos = str(i+1)

            print(pos + "-  " + str(rev_keys[i]) + " ::: " + str(rev_vals[i]))

    elif pretty == 'd':
        print(indexes)

    elif pretty == 'csv':
        print("", file=open("output.csv", "w"))
        for i in range(dict_len):
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
            if (restockers[i] not in indexed):
                indexed[restockers[i]] = 1
            else:
                indexed[restockers[i]] += 1

def pretty_dict(index):
    pretty = input("Pretty? [y/n/d/csv] :: ")
    if pretty == 'y':
        sort_dict(index, pretty)
    elif pretty == 'n':
        sort_dict(index, pretty)
    elif pretty == 'd':
        sort_dict(index, pretty)
    elif pretty == 'csv':
        sort_dict(index, pretty)

def print_style(index):
    print("\nPrint what data? ")
    print_choice = input("Indexes // Print // Len // Max [1/2/3/4] :: ")

    if print_choice == "1":
        pretty_dict(index)

    elif print_choice == "2":
        print(index)
    
    elif print_choice == "3":
        print(len(index))

    elif print_choice == "4":
        max_key(index)

    else:
        print("\nInvalid input\n")

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
    datalen = range(len(lines_arr))

    # Creates an array with all the users who logged time in the text
    for i in datalen:
        active_users = np.append(active_users, re.sub("\n", "", lines_arr[i])) 
        np.put(active_users, i, re.sub("'s Session Time.+$", "", active_users[i]))
    
    # Makes an array of all logged times in hh:mm:ss
    for i in datalen:
        time_logged = np.append(time_logged, re.sub("\n", "", lines_arr[i])) 
        np.put(time_logged, i, re.sub(".+'s Session Time: ", "",  time_logged[i]))

    # Makes an array of all logged times in seconds
    for i in datalen:
        secs_logged = np.append(secs_logged, get_sec(time_logged[i]))
    
    user_times_secs = dict(zip(active_users, secs_logged))

    # Makes a list of unique users in the dict, indexed
    for i in datalen:
        if active_users[i] not in indexed:
            indexed[active_users[i]] = 0

    # Array of unique users for easy access
    uni_users = list(indexed.keys())
    
    # Pseudocode for time parser
    for i in range(len(uni_users)):
        user = uni_users[i]
        for j in datalen:
            if active_users[j] == user:
                indexed[user] += int(secs_logged[j])

    def secs_to_hms(seconds):
        hours = seconds // (60*60)
        seconds %= (60*60)
        minutes = seconds // 60
        seconds %= 60
        return "%02i:%02i:%02i" % (hours, minutes, seconds)

    total_secs = list(indexed.values())
    for i in range(len(total_secs)):
        total_secs[i] = secs_to_hms(total_secs[i])
        
    # Completed dict with names and total times
    final = dict(zip(uni_users, total_secs))

    print_style(final)

    exit()
    

# Try/Except statement for keyboard interrupt 
try:
    startup()
    file_picker(log)
    # Choose vending/shop/both
#    restock()
#    activity()
    if log != "4": 
        print("\nShow restocks for what? ")
        restock_choice = input("Shop / Vending / Turret / All [1/2/3/4] :: ")

    restock_message = " has just restocked "

    if log == "4":
        time_spent()

    # Restock counting functions for different types
    restock_count("1", "shop", "s", restock_message + "one item in the shop!")
    restock_count("2", "vending", "v", restock_message + "a vending machine!")
    restock_count("3", "turret", "t", restock_message + "a turret!")

    # "Indexes" prints amounts of restocks, "Print" prints all names in order of occurence ... 
    # ...  "Len" prints the number of restocks in that time period
    if log != "timemarch" or log != "4" or log != "tm": 
        print_choice = input("Indexes // Print // Len // Max [1/2/3/4] :: ")

    print_style(indexed)

except KeyboardInterrupt: 
    print("\n\nExiting program...\n")
