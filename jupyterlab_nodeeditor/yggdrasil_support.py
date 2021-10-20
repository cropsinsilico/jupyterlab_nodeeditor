import uuid
import yaml

from .node_editor import NodeEditor

from yggdrasil.examples import yamls as ex_yamls
import jupyterlab_nodeeditor as jlne
import yggdrasil.yamlfile
import re

with open(ex_yamls['fakeplant']['python'], "r") as test_model:
    photosynthesis_model = yaml.safe_load(test_model)['model']
    
# Helper function to make a base empty dictionary
# May not be needed in the future, but will cut time down for now

def new_yggjlne_dict(num_inputs = 1, num_outputs = 1, name = "New Model"):
    inputs, outputs = [], []
    for ins in range(num_inputs):
        inputs.append({'title': '', 'key': '', 'socket_type': ''})
    for outs in range(num_outputs):
        outputs.append({'title': '', 'key': '', 'socket_type': ''})
    return {"inputs": inputs, "outputs": outputs, "title": name}


# Improved version of making a JLNE-compliant dictionary from a Yggdrasil Model YAML
# Still semi-hard coded for the Photosynthesis model
def dict_conversion(model_dict):
    n_ins = len(model_dict["inputs"])
    n_outs = len(model_dict["outputs"])
    # Use the helper function above to make a template
    new_dict = new_yggjlne_dict(n_ins, n_outs, model_dict["name"]) 
    
    # Fill in the Inputs
    for i in range(n_ins):
        new_dict["inputs"][i]["title"] = model_dict["inputs"][i]["name"]
        # Not sure what pattern we should go with for keys, I'll leave it to temp + numbers here
        new_dict["inputs"][i]["key"] = "temp_in" + str(i)
        # This part is slightly hard-coded since default_file doesn't always exist for all Ygg models
        new_dict["inputs"][i]["title"] = model_dict["inputs"][i]["default_file"]["filetype"]
        
    # Fill in the Outputs, same as inputs with name changes
    for o in range(n_outs):
        new_dict["outputs"][o]["title"] = model_dict["outputs"][o]["name"]
        # Not sure what pattern we should go with for keys, I'll leave it to temp + numbers here
        new_dict["outputs"][o]["key"] = "temp_out" + str(o)
        # This part is slightly hard-coded since default_file doesn't always exist for all Ygg models
        new_dict["outputs"][o]["title"] = model_dict["outputs"][o]["default_file"]["filetype"]
           
    return new_dict

# Tesing Code
def load_example(ps = None):
    ps = ps or jlne.NodeEditor()
    dict_conversion(photosynthesis_model)
    ps.add_component(photosynthesis_model)
    return ps

def update_slot(slot):
    rv = {}
    if isinstance(slot, list):
        rv = [update_slot(_) for _ in slot]
        return rv
    elif isinstance(slot, dict):
        rv.update(slot)
        rv.setdefault("title", rv.get("name", ""))
    elif isinstance(slot, str):
        rv.update({"title": slot, "socket_type": "bytes"})
    rv.setdefault("key", rv["title"] + uuid.uuid4().hex)
    rv.setdefault("socket_type", "bytes")
    return rv


def parse_yggdrasil_yaml(fn, node_editor=None):
    if node_editor is None:
        node_editor = NodeEditor()
        node_editor.socket_types = ("bytes",)

    model_db = yaml.load(open(fn, "r"), Loader=yaml.SafeLoader)

    for model in model_db["models"]:
        if "output" in model:
            outputs = update_slot(model["output"])
        elif "outputs" in model:
            outputs = update_slot(model["outputs"])
        if not isinstance(outputs, list):
            outputs = [outputs]
        if "input" in model:
            inputs = update_slot(model["input"])
        elif "inputs" in model:
            inputs = update_slot(model["inputs"])
        if not isinstance(inputs, list):
            inputs = [inputs]
        node_editor.add_component(
            {"title": model["name"], "inputs": inputs, "outputs": outputs}
        )
    return node_editor
