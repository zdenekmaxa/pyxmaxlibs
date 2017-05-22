"""
Python helper functions.

Author: Zdenek Maxa  

"""


import os
import sys
import string
import fnmatch
import random


def print_msg_exit(msg="", exit_code=0):
    """
    Print a message to stdout and exit with specified error code.

    """
    if msg:
        print(msg)
    sys.exit(exit_code)


def get_files(path='.', file_mask=['*'], recursive=False):
    """
    Returns a list of files (excluding links and directories) in
    a specified directory path.
    Check whether each item conforms file_mask or any of multiple
        file masks if provided (file_mask can be a single string
        or list of strings).
    Goes down the directory tree recursively if recursive is True.

    """
    
    def process_directory(dir_path, items):
        """
        Processes files in 1 directory.

        """
        result = []
        for item in items:
            name = os.path.join(dir_path, item)
            if os.path.isfile(name) and not os.path.islink(name):
                for mask in masks:
                    if fnmatch.fnmatch(name, mask):
                        result.append(os.path.abspath(name))
                        break
        return result

    masks = [file_mask] if isinstance(file_mask, str) else file_mask
    assert isinstance(masks, list)

    # final list to be returned, contains all files
    res_list = []
    if recursive:
        for root, dirs, files in os.walk(path):
            files_checked = process_directory(root, files)
            res_list.extend(files_checked)
    else:
        res_list = process_directory(path, os.listdir(path))
    return res_list


def ask_question(msg, answers="[yes/No]", default="no"):
    """
    Prints a question and expects 1 answer from the user in stdin.
    Possible answers specified in the [] list with '/' as separator.
    Valid answer is also first letter of possible answers.

    """
    if answers[0] != '[' or answers[-1] != ']':
        msg = "%s wrongly specified, should be in [] separated by /" % answers
        raise ValueError(msg)

    answer_list = answers[1:-1].split('/')
    
    if len(answer_list) < 2:
        raise ValueError("Too few possible answers: %s" % answers)
    
    answer_list = [item.lower() for item in answer_list[:]]
    default = default.lower()
    
    if default not in answer_list:
        raise ValueError("Default answer %s not among answers: %s" % (default,
                          answers))
    
    print_out = "%s %s: " % (msg, answers)
    print print_out,
   
    inpt = None
    while inpt == None:
        try:
            inpt = raw_input()
        except KeyboardInterrupt:
            print_msg_exit("  KeyboardInterrupt, exit.", exit_code=1)
        except Exception, ex:
            print ex
            inpt = None
            print("  Couldn't recognize the answer, try again.")
            print print_out,
        else:
            inpt = inpt.lower()
            # finally, check what the user answered 
            for i in range(len(answer_list)):
                if inpt == answer_list[i][0] or inpt == answer_list[i]:
                    return answer_list[i]
            else:
                if inpt == '':
                    return default
                else:
                    inpt = None
                    print "  Couldn't recognize the answer, try again."
                    print print_out,


def get_random_string(start, stop, num):
    """
    Returns a random string chosen from a sequence starting at
    start, ending with stop. start/stop must be characters, num is
    lenght of the desired result string.
    Stop character is not included.

    """
    start_int = ord(start)
    stop_int = ord(stop)
    if num < 1 or start_int >= stop_int:
        raise ValueError("Bad arguments:", start, stop, num)

    r = ""
    for i in range(num):
        c = random.randrange(start_int, stop_int)
        r = "".join([r, chr(c)])
    return r
