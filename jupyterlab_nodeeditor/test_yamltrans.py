from unittest import TestCase
import yaml

class TestYamlToEditor(TestCase):
    #check whether the yamltrans function works properly
    
    def get_yaml_from_source(self):
        with open(self.file, "r") as stream:
        try:
            source_yaml=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        source_inputs = source_yaml["model"]["inputs"]
        inputs_ls = []
        input_id = 1
        for input_slot in source_inputs:
            inputs_ls.append(
                "InputSlot(key='int_"
                + str(input_id)
                + "'"
                + ", multi_connection=True, sockets=SocketCollection(), title="
                + "'"
                + input_slot["name"]
                + "'"
                + ")"
            )
            input_id = input_id + 1
        inputs = "inputs=[" + ", ".join(map(str, inputs_ls)) + "]"
        source_outputs = source_yaml["model"]["outputs"]
        outputs_ls = []
        output_id = 1
        for output_slot in source_outputs:
            outputs_ls.append(
                "OutputSlot(key='out_"
                + str(output_id)
                + "'"
                + ", multi_connection=True, sockets=SocketCollection(), title="
                + "'"
                + output_slot["name"]
                + "'"
                + ")"
            )
            output_id = output_id + 1
        outputs = "outputs=[" + ", ".join(map(str, outputs_ls)) + "]"
        
        source_comp = (
        "[Component(controls=[TextInputControlModel(editor=NodeEditorModel(selected_node=None),"
        + "initial_value="
        + "'"
        + source_yaml["model"]["args"]
        + "', key='my_key')],"
        + inputs
        + ","
        + outputs
        + ", sockets=SocketCollection(), title="
        + "'"
        + source_yaml["model"]["name"]
        + "',"
        + "type_name='component_"
        + source_yaml["model"]["name"].lower()
        + "')]"
    )
        self.source_comp=source_comp
    
    def test_yamltrans(self):
        self.assertEqual(jlne.yml_trans(self.file,only_comp=True).repace(" ",""), self.source_comp.repace(" ",""))

if __name__ == '__main__':
    unittest.main()