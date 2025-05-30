from core.autocad_controller import AutoCADController

acadModel = AutoCADController(__name__)

def draw_beam_outline(beam_data, layer_name, origin=(0, 0)):
    
    if acadModel.acad == None:
        return
    
    # Draw outline
    for beam_name in beam_data:
        for span in beam_data[beam_name]:
            if span == "spans":
                continue
            dims = beam_data[beam_name][span]["dimensions"]
            width = dims["width_x"]
            height = dims["height_y"]
            cover = dims["cover"]
            
            points = [
                origin[0], origin[1],
                origin[0] + width, origin[1],
                origin[0] + width, origin[1] + height,
                origin[0], origin[1] + height,
                origin[0], origin[1]
            ]
            
            pline = acadModel.add_lightweight_polyline(points, layer_name)
            pline.Closed = True
            
            # Draw rebars
            rebar_dia = beam_data[beam_name][span]["rebars"]["bottom"]["rebar_dia"]
            rebar_num = beam_data[beam_name][span]["rebars"]["bottom"]["x_dir"]
            radius = rebar_dia/2

            rebar_coord_x = origin[0] + cover + radius
            rebar_coord_y = origin[1] + cover + radius
            rebar_spacing = (width - 2 * (radius + cover)) / (rebar_num - 1)
            for i in range(rebar_num):
                circle = acadModel.add_circle((rebar_coord_x, rebar_coord_y), radius, layer_name)    
                hatch = acadModel.add_hatch()
                acadModel.append_outer_loop(circle, hatch)
                hatch.Evaluate()
                rebar_coord_x += rebar_spacing
            
            
            
            
            
            
            