from yggdrasil.examples import yamls as ex_yamls
import yaml
import jupyterlab_nodeeditor as jlne

# Improved version of making a JLNE-compliant dictionary from a Yggdrasil Model YAML
# Still semi-hard coded for the Photosynthesis model
# TO-DO : Make more robust, Test on custom models
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

# Tesing Code
# By default, load the photosynthesis model
# ps - Node Editor instance that it is added to, default blank
# TO-DO :
# Add more tests and update as custom models are built
def load_example(ps = None):
    with open(ex_yamls['fakeplant']['python'], "r") as test_model:
        photosynthesis_model = yaml.safe_load(test_model)['model']
        
    ps = ps or jlne.NodeEditor()
    
    # Add in the converted dictionary of the photosynthesis model
    ps.add_component(dict_conversion(photosynthesis_model))
    return ps