import jupyterlab_nodeeditor as jlne
from yggdrasil import yamlfile
import yaml
from collections import OrderedDict
from collections import defaultdict

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
    comps, instances, conns = transform(model_set, coll, editor)

    if text_only:
        return comps
    else:
        for comp in comps:
            editor.add_component(comp)
    if show_instance:
        for instance in instances:
            editor.node_editor.nodes = editor.node_editor.nodes + [instance]
        for conn in conns:
            editor.node_editor.connections = editor.node_editor.connections + [conn]
        editor.node_editor.send({'name': 'arrangeNodes'})
    return editor


def transform(model_set, coll, editor):
    all_comps = []
    all_instances = []
    model_id = 1
    inst_dict = {}
    for model in model_set["models"]:
        args = model["args"]
        model_name = model["name"]
        inputs = {}
        outputs = {}

        ## currently we only consider inputs/outputs contains on input/output
        for input__ in model["inputs"]:
            temp_input = input__["name"].split(":")[1]
            if "is_default" in input__.keys():
                continue
            else:
                input_default_file= OrderedDict({k: input__["default_file"][k] for k in ( 'filetype','name') if k in input__["default_file"]})
                inputs[temp_input] = input_default_file

        for output__ in model["outputs"]:
            temp_output = output__["name"].split(":")[1]
            if "is_default" in output__.keys():
                continue
            else:
                output_default_file = OrderedDict({k: output__["default_file"][k] for k in ('filetype','name') if k in output__["default_file"]})
                outputs[temp_output] = output_default_file

        ## we create the ints and outs below at the end return the nodes
        input_param = 1
        output_parm = 1
        input_ls = []
        output_ls = []
        ports_dict = {}  # store all the port name and key for connection purpose

        # print(outputs)
        for input_,input_file_path in inputs.items():
            locals()["int_{}".format(input_param)] = jlne.InputSlot(
                title=input_,
                key="int_{}".format(input_param),
                sockets=coll,
                multi_connection=True,
                default_file=input_file_path,
            )
            ports_dict[input_] = "int_{}".format(input_param)
            input_ls.append(locals()["int_{}".format(input_param)])
            input_param = input_param + 1

        for output_,output_file_path in outputs.items():
            locals()["out_{}".format(output_parm)] = jlne.OutputSlot(
                title=output_,
                key="out_{}".format(output_parm),
                sockets=coll,
                multi_connection=True,
                default_file=output_file_path,
            )
            ports_dict[output_] = "out_{}".format(output_parm)
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
        ports_dict["node_inst"] = locals()["inst_{}".format(model_id)]
        inst_dict[model_name] = ports_dict
        model_id = model_id + 1

    all_conns = []
    for conn in model_set["connections"]:
        # print(conn)
        src_model_ls = conn["src_models"]

        if src_model_ls == []:
            scr_models = []
            scr_model_info = {}
            file_add = conn["inputs"][0]["name"]
            out1 = jlne.OutputSlot(
                title="load_file", key="out_1", sockets=coll, multi_connection=True
            )
            contrl1 = jlne.TextInputControlModel(
                key="my_key", editor=editor.node_editor, value=file_add
            )
            input_file_comp = jlne.Component(
                sockets=coll, outputs=[out1], controls=[contrl1], title="Input_File"
            )
            input_file_inst = jlne.node_editor.NodeInstanceModel(
                sockets=coll, title="Input_File", outputs=[out1], controls=[contrl1]
            )

            all_comps.append(input_file_comp)
            all_instances.append(input_file_inst)

            ## for building connections (source_node, no existing comp)
            src_model = input_file_inst
            src_key = "out_1"
            scr_model_info["source_node"] = src_model
            scr_model_info["source_key"] = src_key
            scr_models.append(scr_model_info)

        else:
            scr_models = []
            for src_model_id in range(len(src_model_ls)):
                scr_model_info = {}
                src_model_name = conn["src_models"][src_model_id]
                src_port = conn["inputs"][src_model_id]["name"].split(":")[1]
                src_model = inst_dict[src_model_name]["node_inst"]
                src_key = inst_dict[src_model_name][src_port]
                scr_model_info["source_node"] = src_model
                scr_model_info["source_key"] = src_key
                scr_models.append(scr_model_info)

        dst_model_ls = conn["dst_models"]
        if dst_model_ls == []:
            dst_models = []
            dst_model_info = {}
            file_add = conn["outputs"][0]["name"]
            in1 = jlne.InputSlot(
                title="export_file", key="in_1", sockets=coll, multi_connection=True
            )
            contrl1 = jlne.TextInputControlModel(
                key="my_key", editor=editor.node_editor, value=file_add
            )
            export_file_comp = jlne.Component(
                sockets=coll, inputs=[in1], controls=[contrl1], title="Export_File"
            )
            export_file_inst = jlne.node_editor.NodeInstanceModel(
                sockets=coll, title="Export_File", inputs=[in1], controls=[contrl1]
            )

            all_comps.append(export_file_comp)
            all_instances.append(export_file_inst)

            ## for building connections (source_node, no existing comp)
            dst_model = export_file_inst
            dst_key = "in_1"
            dst_model_info["destination_node"] = dst_model
            dst_model_info["destination_key"] = dst_key
            dst_models.append(dst_model_info)

        else:
            dst_models = []
            for dst_model_id in range(len(dst_model_ls)):
                dst_model_info = {}
                dst_model_name = conn["dst_models"][dst_model_id]
                dst_port = conn["outputs"][dst_model_id]["name"].split(":")[1]
                dst_model = inst_dict[dst_model_name]["node_inst"]
                dst_key = inst_dict[dst_model_name][dst_port]
                dst_model_info["destination_node"] = dst_model
                dst_model_info["destination_key"] = dst_key
                dst_models.append(dst_model_info)

        for src_model in scr_models:
            for dst_model in dst_models:
                new_connection = jlne.node_editor.ConnectionModel(
                    source_node=src_model["source_node"],
                    source_key=src_model["source_key"],
                    destination_node=dst_model["destination_node"],
                    destination_key=dst_model["destination_key"],
                )
                all_conns.append(new_connection)
    return all_comps, all_instances, all_conns




def parse_editor_config(py_models_dict, editor_json):
    model_ls = []
    if "id" in editor_json.keys():
        node_ids = editor_json["nodes"].keys()
    else:
        node_ids = editor_json[list(editor_json.keys())[0]]["nodes"].keys()
    added_models = []

    for node_id in node_ids:

        single_model_dict = OrderedDict()  # store a single model

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
        
        single_model_dict["name"] = model_name
        # for test purpose
        single_model_dict["language"] = "python"
        single_model_dict["args"] = py_models_dict[str(model_id)]["args"]

        input_ls = []
        output_ls = []

        inputs = list(py_models_dict[str(model_id)]["inputs"])
        for model_input in inputs:
            single_port = OrderedDict()
            single_port["name"] = model_name + ":" + model_input.title
            in_ordered_default_file = OrderedDict([
                ('name', model_input.default_file.get("name")),
                ('filetype', model_input.default_file.get("filetype"))
            ])
            single_port["default_file"] = in_ordered_default_file
            input_ls.append(single_port)

        outputs = list(py_models_dict[str(model_id)]["outputs"])
        for model_output in outputs:
            single_port = OrderedDict()
            single_port["name"] = model_name + ":" + model_output.title
            out_ordered_default_file = OrderedDict([
                ('name', model_output.default_file.get("name")),
                ('filetype', model_output.default_file.get("filetype"))
            ])
            single_port["default_file"] = out_ordered_default_file
            output_ls.append(single_port)

        if len(input_ls) != 0:
            single_model_dict["inputs"] = input_ls
        if len(output_ls) != 0:
            single_model_dict["outputs"] = output_ls
        

        if model_name not in added_models:
            added_models.append(model_name)
            model_ls.append(single_model_dict)
    return model_ls


def merge_list_of_dictionaries(dict_list):
    new_dict = {}
    for d in dict_list:
        for d_key in d:
            if d_key not in new_dict:
                new_dict[d_key] = []
            new_dict[d_key].append(d[d_key])
    return new_dict


def merge_keys(d):
    merged = defaultdict(list)
    for k, v in d.items():
        merged[v[0]].append(k)

    return merged

class IndentedDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentedDumper, self).increase_indent(flow, False)

def represent_ordereddict(dumper, data):
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

IndentedDumper.add_representer(OrderedDict, represent_ordereddict)

def editor_yaml(editor, address):
    editor.node_editor.sync_config()
    editor_json = editor.node_editor.editorConfig
    editor_py = editor.node_editor.nodes

    if editor_py == []:
        return "No component/instance has been detected in the workspace"
    else:
        py_models_dict = OrderedDict()
        
        for model_pos in range(len(editor_py)):
            single_model = OrderedDict()
            single_model["args"] = editor_py[model_pos].controls[0].value
            single_model["inputs"] = editor_py[model_pos].inputs
            single_model["outputs"] = editor_py[model_pos].outputs
            single_model["model_name"] = editor_py[model_pos].title
            jupyter_id = list(editor_py[0].controls[0].editor.editorConfig.keys())[0]
            
            if "id" == jupyter_id:
                node_id = list(editor_py[0].controls[0].editor.editorConfig["nodes"].keys())[model_pos]
                nodes_info = editor_json["nodes"]
            else:
                node_id = list(editor_py[0].controls[0].editor.editorConfig[jupyter_id]["nodes"].keys())[model_pos]
                nodes_info = editor_json[jupyter_id]["nodes"]
            
            py_models_dict[node_id] = single_model

        node_id_ls = nodes_info.keys()
        all_models = OrderedDict()
        
        for model_id in range(len(editor_py)):
            model_name = editor_py[model_id].title
            in_ports = OrderedDict()
            inputs_ls = editor_py[model_id].inputs
            
            for input_port in inputs_ls:
                in_ports[input_port.key] = input_port.title

            out_ports = OrderedDict()
            outputs_ls = editor_py[model_id].outputs
            
            for output_port in outputs_ls:
                out_ports[output_port.key] = output_port.title

            all_models[model_name] = in_ports
            all_models[model_name]["outputs"] = out_ports

        conn_ls = []
        temp_conn_ls = []
        
        for node_id in node_id_ls:
            output_ports = nodes_info[node_id]["outputs"].keys()

            for output_port in output_ports:
                connect_out_port = nodes_info[node_id]["outputs"][output_port]["connections"]
                
                if len(connect_out_port) >= 1:
                    temp_dst_port = []
                    
                    for out_port_num in range(len(connect_out_port)):
                        dest_node_id = str(connect_out_port[out_port_num]["node"])
                        destination_node_name = py_models_dict[dest_node_id]["model_name"]
                        destination_input_name = all_models[destination_node_name][connect_out_port[out_port_num]["input"]]
                        temp_dst_port.append(destination_node_name + ":" + destination_input_name)
                    
                    source_node_name = py_models_dict[node_id]["model_name"]
                    source_node_output_id = output_port
                    source_node_output_name = all_models[source_node_name]["outputs"][source_node_output_id]

                    conn_input = source_node_name + ":" + source_node_output_name
                    conn_outputs = temp_dst_port

                    for conn_output in conn_outputs:
                        new_conn = OrderedDict([(conn_output, conn_input)])
                        if new_conn not in temp_conn_ls:
                            temp_conn_ls.append(new_conn)

        conn_rm_dup = merge_list_of_dictionaries(temp_conn_ls)
        merged_keys = merge_keys(conn_rm_dup)

        for key, value in merged_keys.items():
            conn_ls.append(OrderedDict([("inputs", key), ("outputs", value)]))
        
        yml_dict = OrderedDict()
        model_ls = parse_editor_config(py_models_dict, editor_json)
        yml_dict["models"] = model_ls
        yml_dict["connections"] = conn_ls

        with open(address, 'w') as outfile:
            yaml.dump(yml_dict, outfile, Dumper=IndentedDumper, default_flow_style=False)
