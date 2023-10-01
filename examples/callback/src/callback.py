import os
from yggdrasil import units, platform
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np
import matplotlib.pyplot as plt

fname = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                     './output/outputCallback.txt')
if os.path.isfile(fname):
    os.remove(fname)

x = [0]
y = [np.random.randn()]
out = widgets.Output()
display(out)

def update_plot(x,y):
    with out:
        clear_output(wait=True)
        plt.plot(x, y)
        plt.show()
    global timer
    timer = threading.Timer(1.0, update_plot)
    timer.start()

def callback_function(msg):
    x.append(x[-1] + 1)
    y.append(units.get_data(msg.args))
    update_plot(x,y)