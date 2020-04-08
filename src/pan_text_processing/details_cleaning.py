import os
import os.path
import re

def cleaning_pan_details(name,fname,pan,dob):
    name = cleaning_name_data(name)
    fname = cleaning_fname_data(fname)
    pan = cleaning_pan_data(pan)
    dob = cleaning_dob_data(dob)

    return name,fname,pan,dob

def cleaning_name_data(name):
    # Cleaning first names, better accuracy
    name = name.rstrip()
    name = name.lstrip()
    name = name.replace("8", "B")
    name = name.replace("0", "D")
    name = name.replace("6", "G")
    name = name.replace("1", "I")
    name = name.replace("!", "I")
    name = re.sub('[^a-zA-Z] +', ' ', name)
    name = ''.join([i if 64 < ord(i) < 91 or ord(i) == 32 else '' for i in name])

    return name

def cleaning_fname_data(fname):

    # Cleaning Father's name
    fname = fname.rstrip()
    fname = fname.lstrip()
    fname = fname.replace("8", "S")
    fname = fname.replace("0", "O")
    fname = fname.replace("6", "G")
    fname = fname.replace("1", "I")
    fname = fname.replace("\"", "A")
    fname = fname.replace("!", "I")
    fname = re.sub('[^a-zA-Z] +', ' ', fname)
    fname = ''.join([i if 64 < ord(i) < 91 or ord(i) == 32 else '' for i in fname])

    return fname

def cleaning_pan_data(pan):
    # Cleaning PAN Card details
    # pan = panline.rstrip()

    pan = pan.rstrip()
    pan = pan.lstrip()
    pan = pan.replace(" ", "")
    pan = pan.replace("\"", "")
    pan = pan.replace("/", "J")
    pan = pan.replace(";", "")
    pan = pan.replace("%", "L")
    pan = pan.replace("l", "I")
    pan = ''.join([i if 47 < ord(i) < 58 or 64 < ord(i) < 91 or ord == 45 else '' for i in pan])

    # handle numbers in PAN Card Details
    if len(pan) > 9:
        pan = pan[0:10]
        numb = pan[5:9]
        numb = numb.replace('D', '0')
        numb = numb.replace('G', '6')
        numb = numb.replace('O', '0')
        numb = numb.replace('B', '8')
        numb = numb.replace('I', '1')
        pan = pan[:5] + numb + pan[9:]

    return pan

def cleaning_dob_data(dob):

    # Cleaning DOB
    dob = dob.rstrip()
    dob = dob.lstrip()
    dob = dob.replace('l', '/')
    dob = dob.replace('L', '/')
    dob = dob.replace('I', '/')
    dob = dob.replace('i', '/')
    dob = dob.replace('|', '/')
    dob = dob.replace('\"', '/1')
    dob = dob.replace(" ", "")
    dob = ''.join([i if 46 < ord(i) < 58 else '' for i in dob])
    if len(dob) > 10:
        dob = dob[0:10]
        dob = dob[:2] + dob[2].replace('1', '/') + dob[3:]
        dob = dob[:5] + dob[5].replace('1', '/') + dob[6:]

    return dob
