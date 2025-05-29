from utils.files_handler import layers_config, beams_data, columns_data
from core.layer_manager import setup_layers
from core.beams import draw_beam_outline

def main():
    """The main runner function
    """
    
    # Layer Manager
    setup_layers(layers_config)
    
    # Beams Manager
    # draw_beam_outline(beams_data,layer_name="0")
    
    
    
if __name__ == "__main__":
    main()
   