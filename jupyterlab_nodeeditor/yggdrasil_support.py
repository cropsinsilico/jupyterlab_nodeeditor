from yggdrasil.examples import yamls as ex_yamls
import yaml
import jupyterlab_nodeeditor as jlne

# Improved version of making a JLNE-compliant dictionary from a Yggdrasil Model YAML
# Still semi-hard coded for the Photosynthesis model
# TO-DO : Make more robust, Test on custom models 1-3
def dict_conversion(model_dict):
    # Setup initial dictionary to be filled
    new_dict, new_dict["inputs"], new_dict["outputs"], new_dict["title"] = {}, [], [], model_dict["name"]
    
    # Fill in the Inputs
    for i, inp in enumerate(model_dict["inputs"]):
        new_dict["inputs"].append({'title': inp["name"], 'key': "temp_in" + str(i), 'socket_type': inp["default_file"]["filetype"]})
        
    # Fill in the Outputs, same as inputs with name changes
    for o, out in enumerate(model_dict["outputs"]):
        new_dict["outputs"].append({'title': out["name"], 'key': "temp_out" + str(o), 'socket_type': out["default_file"]["filetype"]})
           
    return new_dict

# By default, load the photosynthesis model
# ps - Node Editor instance that it is added to, default blank
def load_example(ps = None):
    with open(ex_yamls['fakeplant']['python'], "r") as test_model:
        photosynthesis_model = yaml.safe_load(test_model)['model']
        
    ps = ps or jlne.NodeEditor()
    
    # Add in the converted dictionary of the photosynthesis model
    ps.add_component(dict_conversion(photosynthesis_model))
    return ps

# Testing Functions

# The first test is just to visually ensure that the model appears in the node editor instance
# This is NOT an explicit function
# Look for Inputs, Outputs, and a proper title

# Test 2 : Verify Editor instance w output
# This is done with JLNE's built in class methods of calling a unique editor instance with the models

# Test 3 : Blank


