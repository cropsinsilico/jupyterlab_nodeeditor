import uuid
import yaml

from .node_editor import NodeEditor

from yggdrasil.examples import yamls as ex_yamls
import jupyterlab_nodeeditor as jlne
import yggdrasil.yamlfile
import re

# Improved version of making a JLNE-compliant dictionary from a Yggdrasil Model YAML
# Still semi-hard coded for the Photosynthesis model
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
def load_example(ps = None):
    with open(ex_yamls['fakeplant']['python'], "r") as test_model:
        photosynthesis_model = yaml.safe_load(test_model)['model']
        
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
