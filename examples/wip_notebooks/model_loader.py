from yggdrasil.examples import yamls as ex_yamls
import yaml
import jupyterlab_nodeeditor as jlne

def dict_conversion(model_file):
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
                        new_dict["inputs"].append({'title': inp["name"], 'key': f"temp_in{i}", 'socket_type': "connection"})
                elif "inputs" in model.keys():
                    for i, inp in enumerate(model["inputs"]):
                        new_dict["inputs"].append({'title': inp["name"], 'key': f"temp_in{i}", 'socket_type': "connection"})
        
                # Fill in the Outputs, same as inputs with name changes
                if "output" in model.keys():
                    for o, out in enumerate(model["output"]):
                        new_dict["outputs"].append({'title': out["name"], 'key': f"temp_out{o}", 'socket_type': "connection"})
                elif "outputs" in model.keys():
                    for o, out in enumerate(model["outputs"]):
                        new_dict["outputs"].append({'title': out["name"], 'key': f"temp_out{o}", 'socket_type': "connection"})
                list_of_models.append(new_dict)
        
        # We return a list here so that way loading the models is uniform for both multi-model and single-model files
        return list_of_models


# ps - Node Editor instance that it is added to, default blank
def load_model(ps = None):
    # Photosynthesis broken right now with tentative changes
    filepath = input("Please enter filepath for model: ")
    
    # Variable that will be used as the processed model
    fsample = None
    
    # Check to see if input is blank or not, run the respective code to get the model from file or the Photosynthesis example
    if filepath:
        with open(filepath, "r") as sample:
            fsample = yaml.safe_load(sample)
            
    # else:
    #     print("Loading Photosynthesis Model into Editor...")
    #     with open(ex_yamls['fakeplant']['python'], "r") as sample:
    #         fsample = yaml.safe_load(sample)["model"]
    
    # This is our socket collection: a list that is converted to a tuple at each instance of adding a component
    socket_list = []
    
    # Convert it all and add it into the editor, then return the entire editor
    
    ne_instance = ps or jlne.NodeEditor()
    
    # Use our conversion/parser to get a list of models
    model_list = dict_conversion(fsample)
    
    # Manually parse the jlne Components due to the bug
    for model in model_list:
        model_ins, model_outs = [], []
        for model_in in model["inputs"]:
            # print("model_in: ", model_in)
            socket_list.append(model_in["socket_type"])
            model_ins.append(jlne.InputSlot(title = model_in["title"], key = model_in["key"], socket_type = model_in["socket_type"], sockets = jlne.SocketCollection(socket_types = tuple(socket_list))))
            
        for model_out in model["outputs"]:
            # print("model_out: ", model_out)
            socket_list.append(model_out["socket_type"])
            model_outs.append(jlne.OutputSlot(title = model_out["title"], key = model_out["key"], socket_type = model_out["socket_type"], sockets = jlne.SocketCollection(socket_types = tuple(socket_list))))
        
        ne_instance.add_component(jlne.Component(sockets = jlne.SocketCollection(socket_types = tuple(socket_list)), inputs = model_ins, outputs = model_outs, title = model["title"]))
    
    return ne_instance