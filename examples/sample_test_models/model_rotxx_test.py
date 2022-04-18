# Input a number for rotation and a string via file
import string

def rotxx_func(x, txt):
    txt_string = "".join(c for c in txt.decode("utf-8").lower() if c in string.ascii_lowercase)
    rotxx = "".join(string.ascii_lowercase[(string.ascii_lowercase.find(s) + x) % 26] for s in txt_string)
    return rotxx
