# Input a number for rotation and a string via file
def rotxx_func(x, txt):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    txt_string = txt.decode("utf-8")

    # It's a one-liner: rotate the string by the number and send it out
    rotxx = "".join([alphabet[(alphabet.find(c) + x) % 26] for c in txt_string])
    return rotxx
