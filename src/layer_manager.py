from autocad_controller import AutoCADController
from files_handler import color_map

acadModel = AutoCADController()

def setup_layers(layers_data: dict) -> None:
    """Create the layers and assign name, color and linetype for each

    Args:
        layers_data (dict): Layers data as dictionary loaded from JSON file or database
    """
    
    for name, props in layers_data.items():
        
        color_name = props.get("color", "white").lower() # Get the layer color, if not exist will be set to "white"
        
        if color_name in color_map["COLOR_MAP"]:
            color_name = color_map["COLOR_MAP"][color_name]
        else:
            color_name = color_map["COLOR_MAP"]["white"]
            print(f"Warning: '{color_name} not mapped, using white.") # GUI_MSG
            
        linetype = props.get("linetype", "Continuous") # Get the layer linetype, if not exist will be set to "Continuous"
        
        description = props.get("description", "")
        
        lineweight = props.get("lineweight", -3)
        
        acadModel.add_layer(name, color_name, linetype, lineweight, description)
    