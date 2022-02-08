import numpy as np
import time
from yggdrasil.interface.YggInterface import YggOutput

if __name__ == '__main__':
    out_file = YggOutput('outputRNG_file')
    fake_timer = 0
    while True:
        if fake_timer == 3:
            break
        rng = np.random.randint(0, 25)
        print(rng)
        out_file.send(rng)
        fake_timer += 1
        time.sleep(10)
