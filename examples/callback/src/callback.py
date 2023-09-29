import os
from yggdrasil import units, platform
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np

fname = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                     './output/outputCallback.txt')
if os.path.isfile(fname):
    os.remove(fname)


def callback_function(msg):
    x = [0]
    y = [np.random.randn()]
    out = widgets.Output()
    display(out)
    with open(fname, 'a') as fd:
        fd.write(str(units.get_data(msg.args)) + platform._newline_str)