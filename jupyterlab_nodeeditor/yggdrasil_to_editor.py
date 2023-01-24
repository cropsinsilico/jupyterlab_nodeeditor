import jupyterlab_nodeeditor as jlne
from yggdrasil import yamlfile


def yml_trans(filename, text_only=False, show_instance=False):
    schema = yamlfile.get_schema()
    socket_types = tuple(
        schema.form_schema["definitions"]["schema"]["definitions"]["simpleTypes"][
            "enum"
        ]
    )
    coll = jlne.SocketCollection(socket_types=socket_types)
    model_set = yamlfile.parse_yaml(filename,model_only=True)
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
            temp_input=input__["name"].split(":")[1]
            if "is_default" in input__.keys():
                continue
            else:
                inputs.append(temp_input)

        for output__ in model["outputs"]:
            temp_output=output__["name"].split(":")[1]
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
