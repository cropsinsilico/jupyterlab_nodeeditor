import yaml
import jupyterlab_nodeeditor as jlne


def _dict_conversion(model_file):
    # If the model type is a list, please notify Het since this shouldn't ever happen
    list_of_models = []

    # Single Model
    if "model" in model_file.keys():
        # Use a variable to story this model dictionary as reference to save a lot of typing
        imodel = model_file["model"]

        # Setup dictionary to be filled
        new_dict, new_dict["inputs"], new_dict["outputs"], new_dict["title"] = (
            {},
            [],
            [],
            imodel["name"],
        )

        # Fill in the Inputs
        for i, inp in enumerate(imodel[list(imodel.keys())[3]]):
            new_dict["inputs"].append(
                {"title": inp["name"], "key": f"temp_in{i}", "socket_type": "bytes"}
            )
        # Fill in the Outputs, same as inputs with name changes
        for o, out in enumerate(imodel[list(imodel.keys())[4]]):
            new_dict["outputs"].append(
                {"title": out["name"], "key": f"temp_out{o}", "socket_type": "bytes"}
            )

        list_of_models.append(new_dict)

    # Multiple Models
    elif "models" in model_file.keys():
        for model in model_file["models"]:
            # Setup dictionary to be filled
            new_dict, new_dict["inputs"], new_dict["outputs"], new_dict["title"] = (
                {},
                [],
                [],
                model[list(model.keys())[0]],
            )

            # Check for singular or multiple in/outputs
            if type(model[list(model.keys())[3]]) is str:
                new_dict["inputs"].append(
                    {
                        "title": model[list(model.keys())[3]],
                        "key": f"temp_in0",
                        "socket_type": "bytes",
                    }
                )
                new_dict["outputs"].append(
                    {
                        "title": model[list(model.keys())[4]],
                        "key": f"temp_out0",
                        "socket_type": "bytes",
                    }
                )
            else:
                for i, inp in enumerate(model[list(model.keys())[3]]):
                    new_dict["inputs"].append(
                        {
                            "title": inp["name"],
                            "key": f"temp_in{i}",
                            "socket_type": "bytes",
                        }
                    )
                for o, out in enumerate(model[list(model.keys())[4]]):
                    new_dict["outputs"].append(
                        {
                            "title": out["name"],
                            "key": f"temp_out{o}",
                            "socket_type": "bytes",
                        }
                    )

            list_of_models.append(new_dict)

    # We return a list here so that way loading the models is uniform for both multi-model and single-model files
    return list_of_models


def load_model(path):
    """
    Load a Yggdrasil model in the form of a YAML file for use in JLNE.

    The function will open a YAML through an inputted filepath and use the built-in parser
    in order to find and turn models into components to be added into a node_editor instance.

    Parameters
    ----------
    path :
        Filepath of the model to parse.

    Returns
    -------
    Tuple of objects
        A tuple of three objects: one is the list of inputs as InputSlot objects, the next is the list of outputs as OutputSlot objects, and finally the socket collection.

    Example Usage
    -------------
    >>> load_model("models_to_parse/photosynthesis.yml")
    """
    # Variable that will be used as the processed model
    fsample = None

    # Check to see if input is blank or not, run the respective code to get the model from file
    if path:
        with open(path, "r") as sample:
            fsample = yaml.safe_load(sample)
    else:
        return f"Error: Invalid filepath {filepath}"

    # This is our socket collection: a list that is converted to a tuple at each instance of adding a component
    socket_list = []
    # Use our conversion/parser to get a list of model inputs/outputs
    model_list = _dict_conversion(fsample)
    model_ins, model_outs = [], []

    # Manually parse the JLNE Components
    for model in model_list:
        for model_in in model["inputs"]:
            socket_list.append(model_in["socket_type"])
            model_ins.append(
                jlne.InputSlot(
                    title=model_in["title"],
                    key=model_in["key"],
                    socket_type=model_in["socket_type"],
                    sockets=jlne.SocketCollection(socket_types=tuple(socket_list)),
                )
            )

        for model_out in model["outputs"]:
            socket_list.append(model_out["socket_type"])
            model_outs.append(
                jlne.OutputSlot(
                    title=model_out["title"],
                    key=model_out["key"],
                    socket_type=model_out["socket_type"],
                    sockets=jlne.SocketCollection(socket_types=tuple(socket_list)),
                )
            )

    return (
        model_ins,
        model_outs,
        jlne.SocketCollection(socket_types=tuple(socket_list)),
    )