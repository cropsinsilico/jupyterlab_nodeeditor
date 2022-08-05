"""
TO DO

Format the code with black

I don't think we should be returning any instances. The model_loader function should merely transform the input yaml into a set of dict objects that can be supplied to add_component. This helps to make sure that the SocketCollection instance that's used by all the different components is the same.

We need to parse the data types being accepted and emitted by the different slots. That means using the default that yggdrasil assumes, if we need to; this is one (of several) instances that relying on yggdrasil's normalization code would be helpful. (@langmm may have thoughts on how to have it fill out the defaults without instantiating any compilation or execution procedures.)

I believe you can considerably simplify the dictionary translation code.
"""



import yaml
import jupyterlab_nodeeditor as jlne

def _dict_conversion(model_file):
    # Use flags to determine model input type
    is_dict, is_list = False, False
    
    # There is no clear indicator if a safeloaded YAML will have single or multiple models
    # List parsing is incomplete at the moment, but all models tested were dictionaries
    
    # If it's neither, return the type so it can be noted and accounted for later
    if type(model_file) is dict:
        is_dict = True
    elif type(model_file) is list:
        is_list = True
    else:
        return ("Unaccounted model type: ", type(model_file))
    
    # This works with both single and multiple model dictionaries
    # If the model type is a list, please notify Het
    if is_dict:       
        list_of_models = []
        
        if "models" in model_file.keys():
            for model in model_file["models"]:
                # Setup dictionary to be filled
                new_dict, new_dict["inputs"], new_dict["outputs"], new_dict['title'] = {}, [], [], model['name']
                
                # Fill in the Inputs
                if "input" in model.keys():
                    for i, inp in enumerate(model["input"]):
                        new_dict["inputs"].append({'title': inp["name"], 'key': f"temp_in{i}", 'socket_type': "bytes"})
                elif "inputs" in model.keys():
                    for i, inp in enumerate(model["inputs"]):
                        new_dict["inputs"].append({'title': inp["name"], 'key': f"temp_in{i}", 'socket_type': "bytes"})
        
                # Fill in the Outputs, same as inputs with name changes
                if "output" in model.keys():
                    for o, out in enumerate(model["output"]):
                        new_dict["outputs"].append({'title': out["name"], 'key': f"temp_out{o}", 'socket_type': "bytes"})
                elif "outputs" in model.keys():
                    for o, out in enumerate(model["outputs"]):
                        new_dict["outputs"].append({'title': out["name"], 'key': f"temp_out{o}", 'socket_type': "bytes"})
                list_of_models.append(new_dict)
        
        # If the key is just "model", that's how we know it is a single model, so no loop needed
        elif "model" in model_file.keys():
            #  model_file["model"].keys() = dict_keys(['name', 'language', 'args', 'inputs', 'outputs'])
            
            # Use a variable to story this model dictionary as reference to save a lot of typing
            imodel = model_file["model"]
            
            # Setup dictionary to be filled
            new_dict, new_dict["inputs"], new_dict["outputs"], new_dict['title'] = {}, [], [], imodel['name']
              
            # Fill in the Inputs
            if "input" in imodel.keys():
                for i, inp in enumerate(imodel["input"]):
                    new_dict["inputs"].append({'title': inp["name"], 'key': f"temp_in{i}", 'socket_type': "bytes"})
            elif "inputs" in imodel.keys():
                for i, inp in enumerate(imodel["inputs"]):
                    new_dict["inputs"].append({'title': inp["name"], 'key': f"temp_in{i}", 'socket_type': "bytes"})
        
            # Fill in the Outputs, same as inputs with name changes
            if "output" in imodel.keys():
                for o, out in enumerate(imodel["output"]):
                    new_dict["outputs"].append({'title': out["name"], 'key': f"temp_out{o}", 'socket_type': "bytes"})
            elif "outputs" in imodel.keys():
                for o, out in enumerate(imodel["outputs"]):
                    new_dict["outputs"].append({'title': out["name"], 'key': f"temp_out{o}", 'socket_type': "bytes"})
            list_of_models.append(new_dict)
        
        # We return a list here so that way loading the models is uniform for both multi-model and single-model files
        return list_of_models
        


# ps - Node Editor instance that it is added to, default blank
def load_model(path = None, ne_instance = None):
    """
    Load a Yggdrasil model in the form of a YAML file for use in JLNE.

    The function will open a YAML through an inputted filepath and use the built-in parser
    in order to find and turn models into components to be used in the Node Editor.

    Parameters
    ----------
    ps : 
        Jupyter Lab Node Editor instance that the models should be added to.

    Returns
    -------
    NodeEditor() instance
        The NodeEditor that was inputted, now with the models as components or a new one if the input was left blank.

    Example Usage
    -------------
    >>> load_model()
    >>> sample_test_models/model_trifecta.yml
    """
    # Default node editor instance and local filepath copy
    if str(type(ne_instance)) != "<class 'jupyterlab_nodeeditor.node_editor.NodeEditor'>":
        return "Error: No Node Editor instance inputted"
    else:
        ps = ne_instance
    filepath = path
    
    # Variable that will be used as the processed model
    fsample = None
    
    # Check to see if input is blank or not, run the respective code to get the model from file
    if filepath:
        with open(filepath, "r") as sample:
            fsample = yaml.safe_load(sample)
    else:
        return f"Error: Invalid filepath {filepath}"
    
    # This is our socket collection: a list that is converted to a tuple at each instance of adding a component
    socket_list = []
    
    # Convert it all and add it into the editor, then return the entire editor  
    ne_instance = ps or jlne.NodeEditor()
    
    # Use our conversion/parser to get a list of models
    model_list = _dict_conversion(fsample)
    
    # Manually parse the jlne Components due to the bug
    for model in model_list:
        model_ins, model_outs = [], []
        for model_in in model["inputs"]:
            socket_list.append(model_in["socket_type"])
            model_ins.append(jlne.InputSlot(title = model_in["title"], key = model_in["key"], socket_type = model_in["socket_type"], sockets = jlne.SocketCollection(socket_types = tuple(socket_list))))
            
        for model_out in model["outputs"]:
            socket_list.append(model_out["socket_type"])
            model_outs.append(jlne.OutputSlot(title = model_out["title"], key = model_out["key"], socket_type = model_out["socket_type"], sockets = jlne.SocketCollection(socket_types = tuple(socket_list))))
        
        ne_instance.add_component(jlne.Component(sockets = jlne.SocketCollection(socket_types = tuple(socket_list)), inputs = model_ins, outputs = model_outs, title = model["title"]))
    
    return ne_instance
