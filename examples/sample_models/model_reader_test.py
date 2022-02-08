from yggdrasil.interface.YggInterface import YggInput, YggOutput

# If we want to do remote reading, we can try reading in the url as its own model
# Then transfer that model to another model to read it in ygg
# This is done locally

if __name__ == '__main__':
    in_file = YggInput('inputReader_file')
    out_file = YggOutput('outputReader_file')
    line_number = 0
    ret = True

    # Output the text line by line with the line number
    while ret:
        (ret, line) = in_file.recv()
        if ret:
            line_number += 1
            ret = out_file.send(line_number, line)
            if not ret:
                raise RuntimeError("ERROR SENDING LINE")
        else:
            print("End of File")
            out_file.send_eof()
