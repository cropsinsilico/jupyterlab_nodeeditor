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

from unittest import TestCase

PASS = "Passed"
FAIL = "Failed"

# I will start with just Photosynthesis model testing, then move on to develop and test custom models

class YggModelTester:

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

# Check to make sure all necessary inputs are accounted for
    def test_inputs(self):
        
