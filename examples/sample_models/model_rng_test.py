import numpy as np
import time
from yggdrasil.interface.YggInterface import YggOutput

if __name__ == '__main__':
    # Setup output file
    out_file = YggOutput('outputRNG_file')

    # This variable is jsut to limit the number of numbers output, can remove if needed
    fake_timer = 0

    # Every 10 seconds, send a random number through the model
    while True:
        if fake_timer == 3:
            break
        rng = np.random.randint(0, 25)
        out_file.send(rng)
        fake_timer += 1
        time.sleep(10)
