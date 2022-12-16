import jupyterlab_nodeeditor as jlne
from yggdrasil import yamlfile


def yml_trans(filename, only_comp=False):
    schema = yamlfile.get_schema()
    socket_types = tuple(
        schema.form_schema["definitions"]["schema"]["definitions"]["simpleTypes"][
            "enum"
        ]
    )
    coll = jlne.SocketCollection(socket_types=socket_types)
    model_set = yamlfile.parse_yaml(filename, model_only=True)
    editor = jlne.NodeEditor(socket_collection=coll)
    comps = transform(model_set, coll, editor)
    if only_comp:
        return comps
    else:
        for comp in comps:
            editor.add_component(comp)
        return editor


def transform(model_set, coll, editor):
    all_nodes = []
    node_id = 1
    for model in model_set["models"]:
        args = model["args"]
        model_name = model["name"]
        inputs = []
        outputs = []

        ## currently we only consider inputs/outputs contains on input/output
        for input__ in model["inputs"]:
            inputs.append(input__["name"].split(":")[1])

        for output__ in model["outputs"]:
            outputs.append(output__["name"].split(":")[1])

        ## we create the ints and outs below. at the end return the nodes
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
            key="my_key", editor=editor.node_editor, initial_value=args[0]
        )

        locals()["comp_{}".format(node_id)] = jlne.Component(
            sockets=coll,
            inputs=input_ls,
            outputs=output_ls,
            controls=[contrl1],
            title=model_name,
        )
        all_nodes.append(locals()["comp_{}".format(node_id)])
        node_id = node_id + 1

    return all_nodes
