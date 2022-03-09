from yggdrasil.interface.YggInterface import YggInput, YggOutput

# If we want to do remote reading, we can try reading in the url as its own model
# Then transfer that model to another model to read it in ygg
# This is done locally

if __name__ == '__main__':
    in_file = YggInput('inputReader')
    out_file = YggOutput('outputReader')
    ret = True

    # Output the text line by line with the line number
    while ret:
        (ret, line) = in_file.recv()
        if ret:
            ret = out_file.send(line)
            if not ret:
                raise RuntimeError("ERROR SENDING LINE")
        else:
            print("End of File")
