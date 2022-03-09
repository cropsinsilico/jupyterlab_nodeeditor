import numpy as np
import time
from yggdrasil.interface.YggInterface import YggOutput

if __name__ == '__main__':
    # Setup output file
    out_file = YggOutput('outputRNG')

    # This variable is just to limit the number of numbers output, can remove if needed
    fake_timer = 0

    # Send 4 numbers through the model
    # TO-DO: Make it so it automatically detects the number of lines
    while True:
        if fake_timer == 4:
            break
        rng = np.random.randint(0, 25)
        out_file.send(rng)
        fake_timer += 1
