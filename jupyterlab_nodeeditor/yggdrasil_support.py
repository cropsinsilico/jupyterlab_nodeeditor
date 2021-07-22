import uuid

import yaml

from .node_editor import NodeEditor


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
