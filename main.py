from re import findall
from re import sub
from sys import maxsize
from os import listdir
from os import rename
from shutil import copyfile
import csv

# TODO: add support for repairing
# TODO: custom time input

### Variables ###
# Welcome message printed on startup
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
command = ""
txt = ""
restock_message = " has just restocked "

r_shop_txt = "has just restocked one item in the shop!"
r_vending_txt = "has just restocked a vending machine!"
r_turret_txt = "has just restocked a turret!"

f_shop_txt = "has just repaired a Door!"
f_vending_txt = "has just repaired a Vending Machine!"
f_turret_txt = "has just repaired a Turret!"

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

### Functions ### 

# Main loop for the program that prints the prompt and handles input
def mainloop():
    global command
    global txt
    global stage_files
    # User input to choose the log

    stage_files = []
    command = input("\n[[p/t/r/h/q]] >>> ")
    
    if command == "p":
        print("\n   Files to parse >> ")
        find_files("trimmed")
        # file_print(stage_files)
        options_print(stage_files)
        file_choice = input("\n     Which file to parse? [#] >> ")
        input_quit(file_choice)
        # Checks to see that the user input was in range
        # otherwise, call main loop again
        try:
            file_to_read = stage_files[int(file_choice) - 1]
            if file_to_read[:8] == "restocks":
                restock_type = input("\n     What restock type? [a/s/v/t] >> ")
                # Quits if 'q' was entered
                input_quit(restock_type)
                if restock_type != "a" and restock_type != "s" and restock_type != "v" and restock_type != "t":
                    print("\n   > Invalid restock type :/\n")
                    mainloop()
                else:
                    # Sets the file based on file choice
                    try:
                        restock_count(file_to_read, restock_type)
                        indexed = {}
                    except:
                        print("\n   > Invalid option selected :/\n")

            if file_to_read[:8] == "repairs-":
                repairs_type = input("\n     What repair type? [a/d/v] >> ")
                # Quits if 'q' was entered
                input_quit(repairs_type)

                if repairs_type != "a" and repairs_type != "d" and repairs_type != "v":
                    print("\n   > Invalid restock type :/\n")
                    mainloop()
                else:
                    # Sets the file based on file choice
                    try:
                        restock_count(file_to_read, repairs_type)
                        indexed = {}
                    except:
                        print("\n   > Invalid option selected :/\n")

            elif file_to_read[:8] == "activity":
                # Calculate time spent based on file selected
                time_spent(file_to_read)
                # Pretty print the returned index
                pretty_dict(indexed)
                indexed = {}
        except IndexError:
            print("\n     > Value out of range :/")
            mainloop()
        except ValueError:
            print("\n     > Invalid option selected :/")
            mainloop()


    # Trims extraneous text from files
    elif command == "t":
        file_num = 1
        print("\n   Files to trim >> ")
        # Prints and numbers the contents of txt_files
        find_files("verbose")
        # file_print(stage_files)
        options_print(stage_files)

        file_trim_choice = input("\n      Which file to trim? [#] >> ")
        if file_trim_choice == 'q':
            mainloop()

        rename_copy = input("\n      Rename or make a copy? [r/c] >> ")
        if rename_copy == 'q':
            mainloop()

        # Checks to see that the user input was in range
        # otherwise, call main loop again
        try:
            file_select = stage_files[int(file_trim_choice) - 1]
        except IndexError:
            print("\n     > Value out of range :/")
            mainloop()
        except ValueError:
            print("\n   > Invalid option selected :/")
            mainloop()

        # Selected file based on the available files and user input
        file_select = stage_files[int(file_trim_choice) - 1]
        # Copies file with _trimmed.txt as the ending
        new_filename = file_select[:-12] + "_trimmed.txt"
        # Renames the selected file to the verbose name generated by filenameprep()
        if rename_copy == "r":            
            rename(file_select, new_filename)
            print("\n   > File successfully renamed!")
            print("   > New file's name: " + new_filename)
        elif rename_copy == "c":
            copyfile(file_select, new_filename)
            print("\n   > File successfully copied!")
            print("   > New file's name: " + new_filename)
        elif rename_copy == 'q':
            mainloop()
        else:
            print(" > Not a valid option :/")
        trim_file(new_filename)

    elif command == "r":
        # Prints all files, if none, escape
        find_files("raw")

        print("     Files to rename >>")
        file_print(stage_files)
        # options_print(stage_files)

        file_choose = input("\n     Which file? [#]  >> ")
        # Quits to mainloop if input is 'q'
        input_quit(file_choose)
        rename_copy = input("\n     Rename or make a copy? [r/c] >> ")
        input_quit(rename_copy)

        try:
            sel_file = stage_files[int(file_choose) - 1]
        except IndexError:
            print("\n     > Value out of range :/")
            mainloop()
        except ValueError:
            print("\n   > Invalid option selected :/")
            mainloop()

        # Finds the verbose file name based on the long form
        verbose_name = truncate_filename(sel_file)

        # Renames the selected file to the verbose name generated by filenameprep()
        if rename_copy == "r":            
            rename(sel_file, verbose_name)
            print("\n     > File successfully renamed!")
            print("       > New file name: " + verbose_name)

        elif rename_copy == "c":
            copyfile(sel_file, verbose_name)
            print("\n     > File successfully copied!")
            print("       > New file's name: " + verbose_name)

        elif rename_copy == 'q':
            mainloop()

        else:
            print("\n     > Invalid option :/")

    # Print help message
    elif command == "helpmeplease":
        options_print()
        mainloop()
    elif command == "h":
        help_text()
    
    elif command == "q":
        print("\n     > Exiting program ...\n")
        exit()

    # Incorrect input
    else:
        print("\n > Not a valid log input :/")

def list_files():
    all_files = []
    curdir = listdir(path='.')
    for curfile in curdir:
        if ".txt" in curfile:
            all_files.append(curfile)
    return all_files

# Startup message
def startup():
    print(welcome)
    # Will try to make a new file
    # If it can prompt user to press h
    # otherwise, do nothing
    try:
        open("help.txt", "x")
        print("Press 'h' for help!")
    except:
        pass
        
# Which file the user will read
def options_print(stage_files):
    if len(stage_files) == 0:
        print("\n > No applicable logs found :/")
        mainloop()
    else:
        file_count = 1
        print("          {}Duration                 Type          Length{}".format(bolds, bolde))
        for i in stage_files:
            data_fields = i.split("_", 7)
            start_date = data_fields[1] + "/" + data_fields[2] + "/" + data_fields[4] 
            end_date = data_fields[4] + "/" + data_fields[5] + "/" + data_fields[6] 
            file_type = first_upper(data_fields[0])
            length_type = first_upper(data_fields[7][:-4])
            print("     {}    {} - {}      {}      {}".format(file_count, start_date, end_date, file_type, length_type))
            file_count += 1
    
# Function to count restocks of whatever is called
# "num", "word", and "char" are used for user input, while "text" is the restock text
def restock_count(command, restock_type):
    global indexed 
    global restockers
    global restock_lines

    # Sets restock_lines equal to all restock notifs in the text
    with open(command, encoding=en) as f:
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

    elif restock_type == "d":
        restock_add(restock_type, "door")
    elif restock_type == "v":
        restock_add(restock_type, "vending")
    elif restock_type == "t":
        restock_add(restock_type, "turret")

    indexed = sort_dict(indexed)
    pretty_dict(indexed)

    restock_lines = []

def restock_add(restock_type, lookfor):
    # Indexes values by restock amount
    for restock_line in restock_lines:
        if lookfor in restock_line:
            user = restock_line.split(" ", 1)[0]
            if (user not in indexed):
                indexed[user] = 1
            else:
                indexed[user] += 1

def truncate_filename(sel_file):
    if "Logistics Department - Logs - " in sel_file:
        log_type = findall("(restock|activity)", sel_file)
        if log_type[0] == "restock":
            log_type = "restocks"
        dates = findall("\d{4}-\d{2}-\d{2}", sel_file)
        months = [dates[0][5:7], dates[1][5:7]] 
        days = [dates[0][-2:], dates[1][-2:]] 
        years = [dates[0][2:4], dates[1][2:4]]
        verbose_name = "{}_{}_{}_{}_{}_{}_{}_verbose.txt".format(log_type, months[0], days[0], years[0], months[1], days[1], years[1])      
        return verbose_name
    elif "Engineering__Technical_-_Logs" in sel_file:
        log_type = findall("(repair|activity)", sel_file)
        if log_type[0] == "repair":
            log_type = "repairs-"
        dates = findall("\d{4}-\d{2}-\d{2}", sel_file)

        months = [dates[0][5:7], dates[1][5:7]] 
        days = [dates[0][-2:], dates[1][-2:]] 
        years = [dates[0][2:4], dates[1][2:4]]
        verbose_name = "{}_{}_{}_{}_{}_{}_{}_verbose.txt".format(log_type, months[0], days[0], years[0], months[1], days[1], years[1])      
        return verbose_name

    else:
        print("Not a valid file to rename! Maybe try to trim the file next?")
    # Original file name: Logistics Department - Logs - restocks-logs [nums] (yyyy-mm-dd to yyyy-mm-dd).txt

# Parameter verbosef: verbose file
# Trims extraneous lines from a log
def trim_file(verbosef):
    if verbosef[:8] == "restocks":
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                if r_shop_txt in line.strip("\n") or r_vending_txt in line.strip("\n") or r_turret_txt in line.strip("\n"): 
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
        print("   > File trimmed successfully!")

    elif verbosef[:8] == "repairs-":
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                if f_shop_txt in line.strip("\n") or f_vending_txt in line.strip("\n") or f_turret_txt in line.strip("\n"): 
                    f.write(line)

        # Second go-around, replacing verbose restock message with truncated one
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                username = line.split(" ", 1)[0]
                repairs_text = line.split(" ", 1)[1]

                if "Door!" in repairs_text:
                    repairs_text = " door\n"
                elif "Machine!" in repairs_text:
                    repairs_text = " vending\n"
                # elif "turret!" in restock_text:
                #    restock_text = " turret\n"
                f.write(username + repairs_text)
        print("   > File trimmed successfully!")

    elif verbosef[:8] == "activity":
        with open(verbosef, "r", encoding=en) as f:
            lines = f.readlines()
        with open(verbosef, "w", encoding=en) as f:
            for line in lines:
                if "'s Session Time: " in line.strip("\n"): 
                    if "> " not in line:
                        f.write(line)
                    else:
                        line = sub("> ", "", line)
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

def find_files(stage):
    txt_files = list_files()
    global stage_files
    
    if stage == "raw":  
        for txt_file in txt_files:
            if "Logistics Department - Logs -" in txt_file or 'Engineering__Technical_-_Logs' in txt_file:
                stage_files.append(txt_file)
    elif stage == "verbose":  
        for txt_file in txt_files:
            if "_verbose.txt" in txt_file:
                stage_files.append(txt_file)
    elif stage == "trimmed":  
        for txt_file in txt_files:
            if "_trimmed.txt" in txt_file:
                stage_files.append(txt_file)
    
    return stage_files

# Stylized printing loop for stage_files outputted from file_print
def file_print(files_arr):
    file_num = 1

    # Checks that the txt_files contains something
    if len(files_arr) == 0:
        print("\n > No applicable logs found :/")
        mainloop()
    else:
        for txt_file in files_arr:
            print("     {}[{}]{}--     {}".format(bolds, file_num, bolde, txt_file))
            file_num += 1

# Prints based on stage of the file
# Called in file_print(stage)
def print_options(print_type, must_contain):
    for txt_file in txt_files:
        if must_contain in txt_file:
            stage_files.append(txt_file)

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

def pretty_dict(dict1):
    pretty = input("\n     Pretty print? [y/n/csv] >> ")

    if pretty == 'q':
        mainloop()

    if pretty != 'csv':
        num_yn = input("     Number lines? [y/n] >> ")
        if num_yn == 'q':
            mainloop()
            
    keys = list(dict1.keys())
    vals = list(dict1.values())
    max_len = len(keys[0])

    
    for j in range(len(dict1)):
        if len(keys[j]) > max_len:
            max_len = len(keys[j])
        
    if pretty == 'y':
        print("\n")
        for i in range(len(dict1)):
            if i+1 < 10:
                pos = "00" + str(i+1)
            elif i+1 < 100: 
                pos = "0" + str(i+1) 
            else:
                pos = str(i+1)

            spaces = int((max_len - len(keys[i])) + 6) * " "
            
            if num_yn == 'y':
                print(pos + ".    " + str(keys[i]) + spaces + str(vals[i]))
            elif num_yn == 'n':
                print(str(keys[i]) + spaces + str(vals[i]))

    elif pretty == 'n':
        print(dict1)

    elif pretty == 'csv':
        with open('output.csv', 'w') as f:  
            writer = csv.writer(f)
            for k, v in dict1.items():
                writer.writerow([k, v]) 
        print("\n   > CSV successfully written to output.csv!")

def get_sec(time_str):
    try:
        time_str = sub("[hms]", "", time_str)
        h, m, s = time_str.split(':')
        return int(int(h) * 3600 + int(m) * 60 + int(s))
    except ValueError:
        return 0

def time_spent(command):
    global active_users
    global time_logged
    global secs_logged
    global indexed
    
    with open(command, encoding=en) as f:
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

    # After adding all the seconds, we sort it
    indexed = sort_dict(indexed)
    
    # Array of unique users and total_seconds
    uni_users = list(indexed.keys())
    total_secs = list(indexed.values())

    for i in range(len(total_secs)):
        total_secs[i] = secs_to_hms(total_secs[i])
        
    # Completed dict with names and total times
    indexed = dict(zip(uni_users, total_secs))

    return indexed

# Converts an int (seconds) into a string formatted in hh:mm:ss
def secs_to_hms(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

def help_text():
        print("\n     -----------------------------------------------------------------")
        print("     p -- {}Print/parse{}: reads a trimmed file and outputs data".format(bolds, bolde))
        print("     t -- {}Trim{}: trims a longer file for faster parsing times".format(bolds, bolde))
        print("     r -- {}Rename{}: renames the longer file names".format(bolds, bolde))
        print("     h -- {}Help{}: prints this help text (how would you get here?)".format(bolds, bolde))
        print("     q -- {}Quit{}: quits the program, will return to prompt if in command".format(bolds, bolde))
        print("     > Flow of commands should be: {}r{} and {}t{} initially then {}p{} afterwards".format(bolds, bolde, bolds, bolde, bolds, bolde))
        print("     -----------------------------------------------------------------")

def input_quit(user_input):
    if user_input == 'q':
        mainloop()

# Returns a string with the first letter capitalized
def first_upper(string):
    string = string[0].upper() + string[1:]
    return string

# Try/Except statement for keyboard interrupt 
try:
    # Startup message from welcome sting
    startup()
    while True:
        
        # Removed stage files from previous command
        stage_files = []
        # Remove previous values from indexed
        indexed = {}
        # Call mainloop
        mainloop()
        indexed = {}

except KeyboardInterrupt: 
    print("\n\n     > Exiting program ...\n")
