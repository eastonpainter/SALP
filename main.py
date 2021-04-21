import re
import numpy as np
from sys import maxsize
from os import listdir
from os import rename
from shutil import copyfile
from time import sleep
# import march

# User input for log choice
# TODO: add custom .txt input
# TODO: add processing for time and repairs
# TODO: custom time input
# TODO: finish GUI
# TODO: add total restocks
# TODO: add command support
# TODO: organize ++ improve functions

# Functions #
#startup():
#options_print():
#file_picker(log, txt):
#trim_file():
#max_key(dict1):
#sort_dict(indexes):
#restock_count(num, word, char, text):
#pretty_dict(index):
#print_style(index):
#get_sec(time_str):
#time_spent():
#secs_to_hms(seconds):

# Untruncates numpy array output
np.set_printoptions(threshold=maxsize)

### Variables ###
welcome = """*
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
< ---------------------------------- >"""
bolds = '\033[1m'
bolde = '\033[0m'

# Encoding type for the file opens, utf8 for compatability
en = 'utf8'
log = ""
txt = ""
restock_message = " has just restocked "

shop_txt = "has just restocked one item in the shop!"
vending_txt = "has just restocked a vending machine!"
turret_txt = "has just restocked a turret!"

# Indexed dict containing all usernames and occurences of said usernames
indexed = {}

# List of restocks
restockers = []

restock_lines = []
activity_lines = []

# Logged time arrays for users, time, and time in seconds
active_users = []
time_logged = []
secs_logged = []

# Stage files contains all applicable files based on selected stage
stage_files = []

def list_files():
    all_files = []
    curdir = listdir(path='.')
    for curfile in curdir:
        if ".txt" in curfile:
            all_files.append(curfile)
    return all_files

txt_files = list_files()

### Functions ### 

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
    print("P-- print    R-- rename    T-- trim    H-- help")

# Prints based on stage of the file
# Called in print_files(stage)
def print_options(print_type, must_contain):
    for txt_file in txt_files:
        if must_contain in txt_file:
            stage_files.append(txt_file)

def print_files(stage):
    txt_files = list_files()
    global stage_files
    file_num = 1
    
    if stage == "raw":  
        for txt_file in txt_files:
            if "Logistics Department - Logs -" in txt_file:
                stage_files.append(txt_file)
    elif stage == "verbose":  
        for txt_file in txt_files:
            if "_verbose.txt" in txt_file:
                stage_files.append(txt_file)
    elif stage == "trimmed":  
        for txt_file in txt_files:
            if "_trimmed.txt" in txt_file:
                stage_files.append(txt_file)

    # Checks that the txt_files contains something
    if len(txt_files) == 0:
        print("\n > No applicable logs found :/")
    else:
        for txt_file in stage_files:
            print("{}[{}]{}--     {}".format(bolds, file_num, bolde, txt_file))
            file_num += 1

def file_picker():
    global log
    global txt
    global stage_files
    # User input to choose the log

    stage_files = []
    log = input("\n[[p/r/t/c/h/q]] >>> ")
    
    if log == "p":
        print("\nFiles to parse >> ")
        print_files("trimmed")
        if len(stage_files) == 0:
            print("\n > No files found :/")
        else:
            file_choice = input("\nWhich file to parse? [#] >> ")
            try:
                file_to_read = stage_files[int(file_choice) - 1]
            except IndexError:
                print("\n > Value out of range\n")
                exit()

            if file_to_read[:8] == "restocks":
                restock_type = input("\nWhat restock type? [a/s/v/t] >> ")
                if isinstance(int(file_choice), int) and int(file_choice) <= len(stage_files):
                    if restock_type != "a" and restock_type != "s" and restock_type != "v" and restock_type != "t":
                        print("Invalid restock type :/")
                    else:
                        # Sets the file based on file choice
                        restock_count(file_to_read, restock_type)
                else:
                    print("\nInvalid file choice :/")
            else:
                time_spent(file_to_read)
    # March logs input
#    elif log == "mar" or log == "1" or log == "m1":
#        with open('restock-logs2021-03-21-to-2021-03-28.txt', 'r', encoding=en) as file:
#            txt = file.read()

    # Custom file selection
    elif log == "c":
        file_choice = input("Enter file name >> ")
        try:
            with open(file_choice, 'r', encoding=en) as file:
                txt = file.read()
        except:
            print("\nError! Something went wrong :/")

    # Trims files
    elif log == "t":
        file_num = 1
        print("Text files in current directory >> \n")
        # Prints and numbers the contents of txt_files
        print_files("verbose")
        if len(txt_files) == 0 or len(stage_files) == 0:
            print("\nNo applicable files found :/")
        else:
            file_trim_choice = input("\nWhich file to trim? [#] >> ")

            rename_copy = input("\nRename or make a copy? [r/c] >> ")
            # Verifies that the choice was not greater than the max and not smaller than one
            if int(file_trim_choice) > len(stage_files) or int(file_trim_choice) < 1:
                print("\nCannot select file-- out of range.")
            else:
                # Selected file based on the available files and user input
                sel_file = stage_files[int(file_trim_choice) - 1]
                # Copies file with _trimmed.txt as the ending
                new_filename = sel_file[:-12] + "_trimmed.txt"
                # Renames the selected file to the verbose name generated by filenameprep()
                if rename_copy == "r":            
                    rename(sel_file, new_filename)
                    print("\n > File successfully renamed!")
                    print(" > New file's name: " + new_filename)
                elif rename_copy == "c":
                    copyfile(sel_file, new_filename)
                    print("\n > File successfully copied!")
                    print(" > New file's name: " + new_filename)
                else:
                    print(" > Not a valid option :/")
                trim_file(new_filename)
        stage_files = []
#            except Exception as error:
#                print(error)
    elif log == "r":
        # Retrieves all text files from curdir
        
        # Prints all files, if none, escape
        print_files("raw")
        if len(txt_files) == 0:
            pass
        else:
            file_choose = input("\nWhat file would you like to rename/copy? >> ")
            rename_copy = input("\nRename or make a copy? [r/c] >> ")
            try:
                if int(file_choose) > len(txt_files) and int(file_choose) > 0:
                    print("\nCannot select file; out of range.")
                else:
                    sel_file = stage_files[int(file_choose) - 1]
                    verbose_name = filename_prep(sel_file)
                    # Renames the selected file to the verbose name generated by filenameprep()
                    if rename_copy == "r":            
                        rename(sel_file, verbose_name)
                        print("\nFile successfully renamed!")
                    elif rename_copy == "c":
                        copyfile(sel_file, verbose_name)
                        print("\nFile successfully copied!")
                    else:
                        print(" > Not a valid option :/")
            except:
                print("Error")

    # Print help message
    elif log == "h":
        options_print()
        file_picker()
    
    elif log == "q":
        print("\nExiting program...\n")
        exit()

    # Incorrect input
    else:
        print("\n > Not a valid log input :/")

def filename_prep(sel_file):
    if "Logistics Department - Logs - " in sel_file:
        log_type = re.findall("(restock|activity)", sel_file)
        if log_type == "restock":
            log_type = "restocks"
        dates = re.findall("\d{4}-\d{2}-\d{2}", sel_file)
        months = [dates[0][5:7], dates[1][5:7]] 
        days = [dates[0][-2:], dates[1][-2:]] 
        years = [dates[0][2:4], dates[1][2:4]]
        verbose_name = "{}_{}_{}_{}_{}_{}_{}_verbose.txt".format(log_type[0], months[0], days[0], years[0], months[1], days[1], years[1])      
        return verbose_name
    else:
        print("Not a valid file to rename! Maybe try to trim the file next?")
    # Original file name: Logistics Department - Logs - restocks-logs [nums] (yyyy-mm-dd to yyyy-mm-dd).txt

# Parameter verbosef: verbose file
# Trims extraneous lines from a log
def trim_file(verbosef):
    shop = "has just restocked one item in the shop!"
    vending = "has just restocked a vending machine!"
    turret = "has just restocked a turret!"
    if verbosef[:8] == "restocks":
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                if shop in line.strip("\n") or vending in line.strip("\n") or turret in line.strip("\n"): 
                    f.write(line)

        # Second go-around, replacing verbose restock message with truncated one
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                username = line.split(" ", 1)[0]
                restock_text = line.split(" ", 1)[1]
                if "shop!" in restock_text:
                    restock_text = " shop\n"
                elif "vending" in restock_text:
                    restock_text = " vending\n"
                elif "turret!" in restock_text:
                    restock_text = " turret\n"
                f.write(username + restock_text)
        print(" > File trimmed successfully!")

    elif verbosef[:8] == "activity":
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                if "'s Session Time: " in line.strip("\n"): 
                    if "> " not in line:
                        f.write(line)
                    else:
                        line = re.sub("> ", "", line)
                        f.write(line)
        
        # Second go-around, trimming and converting time to secs
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                line_parts = line.split(" ", 3)
                username = line_parts[0][:-2]
                hms_time = get_sec(line_parts[3])
#                f.write(username + restock_text)
                f.write(username + " " + str(hms_time) + "\n")
    else:
        print("Invalid option")

# Finds maximum key of inputted dictionary and outputs it with username
def max_key(dict1):
    max1 = list(indexed.values())[0]
    user = ''
    # What is this? Lisp?
    for i in range(len(list(dict1.values()))):
        if list(dict1.values())[i] > max1:
            max1 = list(dict1.values())[i]
            user = list(dict1)[i]
    return user, max1 

def sort_dict(indexes):
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
    return final

# Function to count restocks of whatever is called
# "num", "word", and "char" are used for user input, while "text" is the restock text
def restock_count(log, restock_type):
    global indexed 
    global restockers

    # Sets restock_lines equal to all restock notifs in the text
    with open(log, encoding=en) as f:
        for line in f:
            restock_lines.append(line.strip("\n"))
    
    if restock_type == "a":
        # Indexes values by restock amount
        for restock_line in restock_lines:
            user = restock_line.split(" ", 1)[0]
            if (user not in indexed):
                indexed[user] = 1
            else:
                indexed[user] += 1

    elif restock_type == "s":
        restock_add(restock_type, "s")
    elif restock_type == "v":
        restock_add(restock_type, "v")
    elif restock_type == "t":
        restock_add(restock_type, "t")

    
    with open(log, encoding=en) as f:
        for line in f:
            print(line) 

    print(indexed)

def restock_add(restock_type, lookfor):
    # Indexes values by restock amount
    for restock_line in restock_lines:
        if lookfor in restock_line:
            user = restock_line.split(" ", 1)[0]
            if (user not in indexed):
                indexed[user] = 1
            else:
                indexed[user] += 1

def pretty_dict(dict1):
    pretty = input("Pretty print? [y/n/csv] >> ")
    keys = list(dict1.keys())
    vals = list(dict1.values())
    max_len = len(keys[0])

    for j in range(len(dict1)):
        if len(keys[j]) > max_len:
            max_len = len(keys[j])
        
    if pretty == 'y':
        for i in range(len(dict1)):
            if i+1 < 10:
                pos = "00" + str(i+1)
            elif i+1 < 100:
                pos = "0" + str(i+1)
            else:
                pos = str(i+1)

            spaces = int((max_len - len(keys[i])) + 6) * " "
            # print(pos + ".    " + str(keys[i]) + spaces + str(vals[i]))
            print(str(keys[i]) + spaces + str(vals[i]))

#            print(pos + "-  " + str(rev_keys[i]) + 10 * " " + str(rev_vals[i]))

    elif pretty == 'n':
        print(indexed)

    elif pretty == 'csv':
        sort_dict(index)
        print("", file=open("output.csv", "w", encoding=en))
        for i in range(len(indexes)):
            print(str(rev_keys[i]) + "," + str(rev_vals[i]), file=open("output.csv", "a", encoding=en))

def get_sec(time_str):
    try:
        time_str = re.sub("[hms]", "", time_str)
        h, m, s = time_str.split(':')
        return int(int(h) * 3600 + int(m) * 60 + int(s))
    except ValueError:
        return 0

def time_spent(log):
    global txt
    global active_users
    global time_logged
    global secs_logged
    global indexed
    
    with open(log, encoding=en) as f:
        for line in f:
            activity_lines.append(line.strip("\n"))
        
    # Creates a dict with unique users and values set to 0 
    for activity_line in activity_lines:
        user = activity_line.split(" ", 1)[0]
        if user not in indexed:
            indexed[user] = 0

    # Adds up total seconds for each user
    for activity_line in activity_lines:
        user = activity_line.split(" ", 1)[0]
        seconds = activity_line.split(" ", 1)[1]

        indexed[user] += int(seconds)

    # Array of unique users and total_seconds
    uni_users = list(indexed.keys())
    total_secs = list(indexed.values())

    for i in range(len(total_secs)):
        total_secs[i] = secs_to_hms(total_secs[i])
        
    # Completed dict with names and total times
    indexed = dict(zip(uni_users, total_secs))

    pretty_dict(indexed)

def secs_to_hms(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

# Try/Except statement for keyboard interrupt 
try:
#startup():
#options_print():
#file_picker():
#trim_file():
#max_key(dict1):
#sort_dict(indexes):
#restock_count(num, word, char, text):
#pretty_dict(index):
#print_style(index):
#get_sec(time_str):
#time_spent():
#secs_to_hms(seconds):
    startup()
    while True:
        stage_files = []
        file_picker()
        # Choose vending/shop/both
        # restock()
        # activity()
        if log == "1" or log == "2" or log == "3": 
            print("Show restocks for what? ")
            restock_choice = input("Shop / Vending / Turret / All [1/2/3/4] >> ")

            restock_count("1", restock_message + "one item in the shop!")
            restock_count("2", restock_message + "a vending machine!")
            restock_count("3", restock_message + "a turret!")

            # "Indexes" prints amounts of restocks, "Print" prints all names in order of occurence ... 
            # ...  "Len" prints the number of restocks in that time period
            print_choice = input("Indexes // Print // Len // Max [1/2/3/4] >> ")

            # Restock counting functions for different types
            print_style(indexed)

        # This path exits the program, if previous, it continues
        if log == "4":
            time_spent()

except KeyboardInterrupt: 
    print("\n\nExiting program...\n")
