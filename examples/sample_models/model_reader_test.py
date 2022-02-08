import urllib
import time

def model_book():
    # Change this to "emit"
    file = urllib.request.urlopen("https://www.gutenberg.org/files/74/74-0.txt")
    i = 0
    for line in file:
        decoded_line = line.decode("utf-8")
        i += 1
        print(i, decoded_line)
        time.sleep(2)
