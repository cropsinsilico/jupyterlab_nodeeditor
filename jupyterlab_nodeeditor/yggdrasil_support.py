import uuid
import yaml

from .node_editor import NodeEditor

import os
import sys
import copy
import pytest
import subprocess
import itertools
import shutil
import logging
from contextlib import contextmanager
from yggdrasil.services import (
    IntegrationServiceManager, create_service_manager_class, ServerError)
from yggdrasil.tests import assert_raises, requires_language
from yggdrasil import runner, import_as_function, platform
from yggdrasil.tools import is_comm_installed, remove_path
from yggdrasil.examples import yamls as ex_yamls
import jupyterlab_nodeeditor as jlne
import yggdrasil.yamlfile
import re

# Coomented out code is testing code, not sure if needed here

# schema = yggdrasil.yamlfile.get_schema()
# socket_types = tuple(schema.form_schema['definitions']['schema']['definitions']['simpleTypes']['enum'])
# default_sockets = jlne.SocketCollection(socket_types = socket_types)
# editor = jlne.NodeEditorModel()

# photosynthesis_model = {}

# # Key note here: always set the model to the actual ['model'] key of the nested dictionary
# with open(ex_yamls['fakeplant']['python'], "r") as test_model:
#     photosynthesis_model = yaml.safe_load(test_model)['model']
    
def create_slot(name, key_name, socket, socket_list, kind):
    if kind == "i":
        return jlne.InputSlot(title = name, key = key_name, socket_type = socket, sockets = socket_list)
    elif kind == "o":
        return jlne.OutputSlot(title = name, key = key_name, socket_type = socket, sockets = socket_list)
    else:
        return "Invalid Slot Kind"

# This is specifically to auto-label the I/Os of the model
# Does NOT clean the filetype extension like .txt, but can be adjusted to do so. 
def clean_string(io_string):
    regex = r'([^/]+$)'
    return re.findall(regex, io_string)[0]

def extract_data(jlne_editor, model, socket_collection):
    # Just getting the title, can easily get the language and filepath if needed.
    name = model['name']

    # Convert I/Os directly to slots
    input_slots = []
    for inputs in model['inputs']:
        input_slots.append(create_slot(inputs['name'], clean_string(inputs['default_file']['name']), inputs['default_file']['filetype'], socket_collection, "i"))
        
    output_slots = []
    for outputs in model['outputs']:
        output_slots.append(create_slot(outputs['name'], clean_string(outputs['default_file']['name']), outputs['default_file']['filetype'], socket_collection, "o"))
        
    # Create the model component and add it to the editor
    jlne_editor.add_component(jlne.Component(sockets = socket_collection, title = name, inputs = input_slots, outputs = output_slots))
    
    return name + " Data Extracted and added to Editor Instance"

# extract_data(editor, photosynthesis_model, default_sockets)



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
