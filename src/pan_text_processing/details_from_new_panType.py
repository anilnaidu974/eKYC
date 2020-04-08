import os
import os.path
import re
import difflib
import csv
import numpy as np


def get_details_for_newPanType(ordered_text,numRE_str,fatherRE_str,dobRE_str):

    pan_line_number = 0
    for wordline in ordered_text:
        xx = wordline.split()
        if ([w for w in xx if re.search(numRE_str, w)]):
            pan_line_number = ordered_text.index(wordline)
            break

    fname_line_number = 0
    for wordline in ordered_text:
        xx = wordline.split()

        if ([w for w in xx if re.search(fatherRE_str, w)]):

            fname_line_number = ordered_text.index(wordline)
            break

    dob_line_number = 0
    for wordline in ordered_text:
        xx = wordline.split()
        if ([w for w in xx if re.search(dobRE_str, w)]):
            dob_line_number = ordered_text.index(wordline)
            break

    name = ordered_text[fname_line_number-1]
    fname = ordered_text[fname_line_number+1]
    pan = ordered_text[pan_line_number+1]
    dob = ordered_text[dob_line_number+1]
    return name,fname,pan,dob