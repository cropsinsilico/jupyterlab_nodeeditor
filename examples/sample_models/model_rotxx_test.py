def rotxx_func(x, txt):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    txt_string = txt.decode("utf-8")
    rotxx = "".join([alphabet[(alphabet.find(c) + x) % 26] for c in txt_string])
    return rotxx
