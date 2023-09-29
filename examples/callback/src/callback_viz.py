import os
import asyncio
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output
from yggdrasil import units, platform

fname = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputCallback.txt')
if os.path.isfile(fname):
    os.remove(fname)

def callback_function(msg):
    x = [0]
    y = [np.random.randn()]
    out = widgets.Output()
    display(out)
    with open(fname, 'a') as fd:
        fd.write(str(units.get_data(msg.args)) + platform._newline_str)

async def update_plot():
    while True:
        await asyncio.sleep(3)
        with out:
            clear_output(wait=True)
            plt.plot(x, y)
            plt.show()

async def process_messages():
    while True:
        await asyncio.sleep(1)
        new_data = float(callback_function(msg))  
        x.append(x[-1] + 1)
        y.append(new_data)
        
# Start the event loop with both coroutines
asyncio.gather(update_plot(), process_messages())
