# Input a number for rotation and a string via file
def rotxx_func(x, txt):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    rotxx = ""
    txt_string = txt.decode("utf-8")
    
    # Rotate letters and lowercase them, leave anything else alone
    for character in txt_string:
        if character.lower() in alphabet:
            rotxx += alphabet[(alphabet.find(character.lower()) + x) % 26]
        else:
            rotxx += character
    
    return rotxx