from pyautocad import APoint
import array
import win32com.client
import pythoncom

def variants(object):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, (object))

def draw_beam_outline(acad, beam_data, layer_name, origin=APoint(0, 0)):
    for beam_name in beam_data:
        for span in beam_data[beam_name]:
            if span == "spans":
                continue
            dims = beam_data[beam_name][span]["dimensions"]
            width = dims["width_x"]
            height = dims["height_y"]
            
            points = [
                origin.x, origin.y,
                origin.x + width, origin.y,
                origin.x + width, origin.y + height,
                origin.x, origin.y + height,
                origin.x, origin.y
            ]
            
            pline = acad.model.AddLightWeightPolyline(array.array("d", points))
            pline.Closed = True
            pline.Layer = layer_name

def draw_rebar(acad, beam_data, layer_name):
    for beam_name in beam_data:
        for span in beam_data[beam_name]:
            if span == "spans":
                continue
            rebar: str = beam_data[beam_name][span]["rebars"]["bottom"]
            rebar_number = int(rebar.split("T")[0]) # FIXME: no hard coded things use regex
            rebar_dia = int(rebar.split("T")[1])/10 # FIXME: no hard coded things use regex
            
            radius = rebar_dia/2
            circle = acad.model.AddCircle(APoint(0, 0), radius)
            circle.Layer = layer_name
            
            # hatch = acad.model.AddHatch(0, "SOLID", False)
            
            # outer = variants([circle])            
            # hatch.AppendOuterLoop(outer)
            # hatch.Evaluate()
            # hatch.Layer = layer_name
            
            