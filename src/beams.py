from autocad_controller import AutoCADController

acadModel = AutoCADController()

def draw_beam_outline(beam_data, layer_name, origin=(0, 0)):
    for beam_name in beam_data:
        for span in beam_data[beam_name]:
            if span == "spans":
                continue
            dims = beam_data[beam_name][span]["dimensions"]
            width = dims["width_x"]
            height = dims["height_y"]
            
            points = [
                origin[0], origin[1],
                origin[0] + width, origin[1],
                origin[0] + width, origin[1] + height,
                origin[0], origin[1] + height,
                origin[0], origin[1]
            ]
            
            pline = acadModel.add_lightweight_polyline(points, layer_name)
            pline.Closed = True
            
def draw_rebar(beam_data, layer_name):
    for beam_name in beam_data:
        for span in beam_data[beam_name]:
            if span == "spans":
                continue
            rebar: str = beam_data[beam_name][span]["rebars"]["bottom"]
            rebar_number = int(rebar.split("T")[0]) # FIXME: no hard coded things use regex
            rebar_dia = float(rebar.split("T")[1])/10 # FIXME: no hard coded things use regex
            
            radius = rebar_dia/2
            circle = acadModel.add_circle((0.0, 0.0, 0.0), radius, layer_name)
            
            