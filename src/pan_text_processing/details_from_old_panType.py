import os
import os.path
import re
import difflib
import csv
import numpy as np

def get_details_from_old_pan(ordered_text,govRE_str,numRE_str):

    pan,dob,pan_line_number = get_pan_dob(ordered_text,numRE_str)
    names_list = get_name_fname_list(ordered_text,govRE_str,pan_line_number)
    name,fname = get_name_fname(names_list)
    return name,fname,pan,dob



def get_pan_dob(ordered_text,numRE_str):
    pan_line_number = 0
    for wordline in ordered_text:
        xx = wordline.split()
        if ([w for w in xx if re.search(numRE_str, w)]):
            pan_line_number = ordered_text.index(wordline)
            break
    pan = ordered_text[pan_line_number + 1]
    pan = pan.replace(" ", "")
    dob = ordered_text[pan_line_number - 1]

    return pan,dob,pan_line_number

def get_name_fname_list(ordered_text,govRE_str,pan_line_number):

    gov_line_number = 0
    names_list = []
    nameline =[]
    for wordline in ordered_text:
        xx = wordline.split()
        if ([w for w in xx if re.search(govRE_str, w)]):
            gov_line_number = ordered_text.index(wordline)
            break
    nameline = ordered_text[gov_line_number + 1:pan_line_number]
    # -----------Read Database
    # namedb_path = '/home/anil/Machine_learning/e-KYC/pan_text_processing/namedb.csv'
    namedb_path = os.path.join(os.getcwd(),"src/pan_text_processing/namedb.csv")

    with open(namedb_path, 'r') as f:
        reader = csv.reader(f)
        newlist = list(reader)
    newlist = sum(newlist, [])

    try:
        for x in nameline:
            for y in x.split():

                if (difflib.get_close_matches(y.upper(), newlist)):
                    names_list.append(x)
                    break
    except Exception as ex:
        pass
    for i, each_name in enumerate(names_list):
        names_list[i] = ''.join([i if 96 < ord(i) < 123 or 64 < ord(i) < 91 or ord(i) == 32 else '' for i in each_name])

    return names_list


def get_name_fname(names_list):
    if (len(names_list) > 1):

        name_fname = sorted(names_list, key=len, reverse=True)[0:2]
        name_fname_indices = [names_list.index(val) for val in name_fname]
        if name_fname_indices[0] > name_fname_indices[1]:
            name = names_list[name_fname_indices[1]]
            fname = names_list[name_fname_indices[0]]
        else:
            name = names_list[name_fname_indices[0]]
            fname = names_list[name_fname_indices[1]]

    else:
        name = names_list[0]
        fname = "NOT FOUND"
    name = ''.join([i if 64 < ord(i) < 91 or ord(i) == 32 else '' for i in name])
    fname = ''.join([i if 64 < ord(i) < 91 or ord(i) == 32 else '' for i in fname])

    # name = names_list[0]
    # name = ''.join([i if 96 < ord(i) < 123 or 64 < ord(i) < 91 or ord(i) == 32 else '' for i in name])
    # fname = names_list[1]
    # fname = ''.join([i if 96 < ord(i) < 123 or 64 < ord(i) < 91 or ord(i) == 32 else '' for i in fname])

    return name, fname

