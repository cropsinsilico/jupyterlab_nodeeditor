# TO-DO
# Transfer Tests from yggdrasil_support.py
# Create more tests to ensure the model was properly put in
# # Test to make sure all important values were extracted
# # # Inputs
# # # Outputs
# # # Title
# # Test all JLNE components added
# # # Slots
# # # Editor
# Make sure Vis is correct (Manual for now as I learn the JLNE output coding)

import uuid
import yaml

from yggdrasil.examples import yamls as ex_yamls
import jupyterlab_nodeeditor as jlne
import yggdrasil.yamlfile

from unittest import TestCase
from yggdrasil_support import *

# I will start with just Photosynthesis model testing, then move on to develop and test custom models

class YggModelTester(TestCase):

# Initialize the Model
    def __init__(self, inputs, outputs, name):
        self.inputs = inputs
        self.outputs = outputs
        self.name = name

# Inputs getter
    @property
    def inputs(self):
        return self.__inputs

# Outputs getter
    @property
    def outputs(self):
        return self.__outputs

# Name getter
    @property
    def name(self):
        return self.__name

# Base calling functions
    def __str__(self):
        return ("YggModelTester(Model Name: %s, Inputs: %s, Outputs: %s)" % (self.name, self.inputs, self.outputs))

    def __repr__(self):
        return self.__str__()

# Get the input model locally
def get_input():
    model = input("Please enter model file name or enter 'example' for a prototype: ")
    if model == "example":
        return load_example()
    infile = open(model, 'r')


def main():
    model_type = input("Please enter 'l' for a local input or 'r' for a remote input model: ")
    if model_type == "l":
        test_model = get_input()
    elif model_type == "r":
        return "Work in Progress"
    else:
        print("Invalid type")
        return main()
        
if __name__ == "__main__":
    main()
