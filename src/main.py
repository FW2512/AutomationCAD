from pyautocad import Autocad
from files_handler import columns_data, layers_config, beams_data
from layer_manager import setup_layers
from beams import draw_beam_outline, draw_rebar

def main():
    """The main runner function"""
    acad = Autocad(create_if_not_exists=True)

    # Setup layers
    setup_layers(acad, layers_config)

    # Draw columns and beams
    draw_beam_outline(acad, beams_data, layer_name="beam_outline")

    # Draw rebar
    draw_rebar(acad, beams_data, layer_name="beam_bottom_rebar")

if __name__ == "__main__":
    main()