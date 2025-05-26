import json


def load_json(path: str) -> dict:
    """Load json files and return the data as dictionary.

    Args:
        path (str): The Path of JSON file.

    Returns:
        dict: Json data as dictionary.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{path} not found!") # GUI_MSG
        return
    except Exception as e:
        print(e) # GUI_MSG
        
layers_config = load_json(r"data\layers_config.json") # GUI_FEATURE: when GUI implemented there maybe an import button to get layers from another project, for now i will hard code the path. # NOTE: must run the script from the main project folder "not src".
beams_data = load_json(r"data\beams_data.json") #GUI_FEATURE: as above
columns_data = load_json(r"data\columns_data.json") #GUI_FEATURE: as above

