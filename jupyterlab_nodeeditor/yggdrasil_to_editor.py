import jupyterlab_nodeeditor as jlne
from yggdrasil import yamlfile
import yaml


def yml_trans(filename, text_only=False, show_instance=False):
    schema = yamlfile.get_schema()
    socket_types = tuple(
        schema.form_schema["definitions"]["schema"]["definitions"]["simpleTypes"][
            "enum"
        ]
    )
    coll = jlne.SocketCollection(socket_types=socket_types)
    model_set = yamlfile.parse_yaml(filename, model_only=True)
    editor = jlne.NodeEditor(socket_collection=coll)
    comps, instances = transform(model_set, coll, editor)

    if text_only:
        return comps
    else:
        for comp in comps:
            editor.add_component(comp)
    if show_instance:
        for instance in instances:
            editor.add_instance(instance)
    return editor


def transform(model_set, coll, editor):
    all_comps = []
    all_instances = []
    model_id = 1
    for model in model_set["models"]:
        args = model["args"]
        model_name = model["name"]
        inputs = []
        outputs = []

        ## currently we only consider inputs/outputs contains on input/output
        for input__ in model["inputs"]:
            temp_input = input__["name"].split(":")[1]
            if "is_default" in input__.keys():
                continue
            else:
                inputs.append(temp_input)

        for output__ in model["outputs"]:
            temp_output = output__["name"].split(":")[1]
            if "is_default" in output__.keys():
                continue
            else:
                outputs.append(temp_output)

        ## we create the ints and outs below at the end return the nodes
        input_param = 1
        output_parm = 1
        input_ls = []
        output_ls = []
        for input_ in inputs:
            locals()["int_{}".format(input_param)] = jlne.InputSlot(
                title=input_,
                key="int_{}".format(input_param),
                sockets=coll,
                multi_connection=True,
            )
            input_ls.append(locals()["int_{}".format(input_param)])
            input_param = input_param + 1

        for output_ in outputs:
            locals()["out_{}".format(output_parm)] = jlne.OutputSlot(
                title=output_,
                key="out_{}".format(output_parm),
                sockets=coll,
                multi_connection=True,
            )
            output_ls.append(locals()["out_{}".format(output_parm)])
            output_parm = output_parm + 1

        contrl1 = jlne.TextInputControlModel(
            key="my_key", editor=editor.node_editor, value=args[0]
        )
        # print(input_ls)
        ## all components
        locals()["comp_{}".format(model_id)] = jlne.Component(
            sockets=coll,
            inputs=input_ls,
            outputs=output_ls,
            controls=[contrl1],
            title=model_name,
        )
        all_comps.append(locals()["comp_{}".format(model_id)])

        ## all instances
        locals()["inst_{}".format(model_id)] = jlne.node_editor.NodeInstanceModel(
            title=model_name,
            inputs=input_ls,
            outputs=output_ls,
            controls=[contrl1],
        )
        all_instances.append(locals()["inst_{}".format(model_id)])
        model_id = model_id + 1

    return all_comps, all_instances


def parse_editor_config(py_models_dict, editor_json):
    model_ls = []
    if "id" in editor_json.keys():
        node_ids = editor_json["nodes"].keys()
    else:
        node_ids = editor_json[list(editor_json.keys())[0]]["nodes"].keys()
    added_models = []

    for node_id in node_ids:

        single_model_dict = {}  # store a single model

        # extracted instance
        if "id" in editor_json.keys():
            inst = editor_json["nodes"][node_id]
        else:
            inst = editor_json[list(editor_json.keys())[0]]["nodes"][node_id]

        model_id = inst["id"]
        model_name = py_models_dict[str(model_id)]["model_name"]

        # store all the node_id and associated model name for later connection match
        inst_dict = {}
        inst_dict[model_id] = model_name

        input_ls = []
        output_ls = []

        inputs = list(py_models_dict[str(model_id)]["inputs"])
        for model_input in inputs:
            single_port = {}
            single_port["name"] = model_name + ":" + model_input.title
            input_ls.append(single_port)

        outputs = list(py_models_dict[str(model_id)]["outputs"])
        for model_output in outputs:
            single_port = {}
            single_port["name"] = model_name + ":" + model_output.title
            output_ls.append(single_port)

        single_model_dict["name"] = model_name
        if len(input_ls) != 0:
            single_model_dict["inputs"] = input_ls
        if len(output_ls) != 0:
            single_model_dict["outputs"] = output_ls

        # for test purpose
        single_model_dict["language"] = "python"
        single_model_dict["args"] = py_models_dict[str(model_id)]["args"]

        if model_name not in added_models:
            added_models.append(model_name)
            model_ls.append(single_model_dict)
    return model_ls


def editor_yaml(editor, address):
    editor.node_editor.sync_config()
    editor_json = editor.node_editor.editorConfig
    # print(editor_json)
    editor_py = editor.node_editor.nodes

    
    if editor_py == []:
        return("No component/instance has been detected in the workspace")
    else:
        py_models_dict = dict()  # extract outputs/inputs/ args information from editor_py
        for model_pos in range(len(editor_py)):
            single_model = dict()
            single_model["args"] = editor_py[model_pos].controls[0].value
            single_model["inputs"] = editor_py[model_pos].inputs
            single_model["outputs"] = editor_py[model_pos].outputs
            single_model["model_name"] = editor_py[model_pos].title
            jupyter_id=list(editor_py[0].controls[0].editor.editorConfig.keys())[0]
            if "id" == jupyter_id:
                node_id = list(editor_py[0].controls[0].editor.editorConfig["nodes"].keys())[model_pos]
            else:
                node_id = list(editor_py[0].controls[0].editor.editorConfig[jupyter_id]["nodes"].keys())[model_pos]
            py_models_dict[node_id] = single_model
        # print(py_models_dict)
        yml_dict = {}  # the keywords for yml_dict include "models" and "connections"
        model_ls = parse_editor_config(py_models_dict, editor_json)
        yml_dict["models"] = model_ls
    
        stream = open(address, "w")
        yaml.dump(yml_dict, stream)
