import os
import os.path
import json
import re

def remove_unordeded_text(text):

    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    ordered_text = []
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        ordered_text.append(s)

    ordered_text = list(filter(lambda x: len(x) > 2, ordered_text))
    ordered_text = list(filter(None, ordered_text))

    return ordered_text