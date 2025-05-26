#################################
## File: src/layer_manager.py ##
################################

COLOR_MAP: dict = {
    "red": 1,
    "yellow": 2,
    "green": 3,
    "blue": 5,
    "white": 7
}
    
def get_existing_linetypes(acad) -> list:
    """Return a list with all the linetypes already loaded to the AutoCAD drawing.

    Args:
        acad (pyautocad.api.Autocad): the pyautocad API for AutoCAD Automation.

    Returns:
        list: List with all the linetypes already loaded to the AutoCAD drawing.
    """
    return [lt.name for lt in acad.doc.Linetypes]

def setup_layers(acad, layers_data: dict) -> None:
    """Create the layers and assign name, color and linetype for each

    Args:
        acad (pyautocad.api.Autocad): the pyautocad API for AutoCAD Automation.
        layers_data (dict): Layers data as dictionary loaded from JSON file or database
    """
    existing_linetypes: list = get_existing_linetypes(acad)
    
    for name, props in layers_data.items():
        try:
            layer = acad.doc.Layers.Item(name) # Check if the layer already exist
            print(f"Layer {name} already exist!") # GUI_MSG
        except: # NOTE: this will catch every error not only the layer exist error "is there another may accure? yeah if the user forget to define a name or invalid layer name (is there any?), maybe somthing else also not sure!" it's better to write specific error moudle for existing layer error.
            layer = acad.doc.Layers.Add(name) # Add the layer
            print(f"Layer {name} created.") # GUI_MSG
        
            color_name = props.get("color", "white").lower() # Get the layer color, if not exist will be set to "white"
            linetype = props.get("linetype", "Continuous") # Get the layer linetype, if not exist will be set to "Continuous"
            
            # Layers Color
            if color_name in COLOR_MAP:
                layer.color = COLOR_MAP[color_name]
            else:
                print(f"Warning: '{color_name} not mapped, using white.") # GUI_MSG
                layer.color = COLOR_MAP["white"]
            
            # Layers Linetype
            try:
                if linetype not in existing_linetypes:
                    acad.doc.Linetypes.Load(linetype, "acad.lin")
                layer.Linetype = linetype
            except Exception as e:
                print(f"Failed to load linetype '{linetype}': {e}.") # GUI_MSG
            
            # Layers Description
            try:
                layer.Description = props.get("description", "")
            except Exception as e:
                print(f"Warning: Failed to set description for layer '{layer}': {e}") # GUI_MSG
            
            # Layers Lineweight
            try:
                layer.Lineweight = props.get("lineweight", -3)
            except Exception as e:
                print(f"Warning: Failed to set lineweight for layer '{name}': {e}") # GUI_MSG
    print("Layer setup complete.") # GUI_MSG
