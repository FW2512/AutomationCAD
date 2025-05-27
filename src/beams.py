from pyautocad import APoint
import array
import win32com.client
import pythoncom

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
            origin.x += width + 10  # shift next beam outline to the right

def draw_beam_rebar(acad, beam_data, layer_name, start_origin=APoint(0, 0)):
    current_x = start_origin.x
    current_y = start_origin.y

    acad_app = win32com.client.Dispatch("AutoCAD.Application")
    doc = acad_app.ActiveDocument
    modelspace = doc.ModelSpace

    for beam_name in beam_data:
        for span in beam_data[beam_name]:
            if span == "spans":
                continue

            dims = beam_data[beam_name][span]["dimensions"]
            width = dims["width_x"]
            height = dims["height_y"]

            rebar = beam_data[beam_name][span]["rebars"]["bottom"]
            rebar_number = int(rebar.split("T")[0])
            rebar_dia = int(rebar.split("T")[1]) / 10
            radius = rebar_dia / 2

            origin_x = current_x
            origin_y = current_y
            spacing = (width - 2 * rebar_dia) / (rebar_number - 1) if rebar_number > 1 else 0

            for i in range(rebar_number):
                x = origin_x + rebar_dia + i * spacing
                y = origin_y + rebar_dia

                center = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, 0))
                circle = modelspace.AddCircle(center, radius)
                circle.Layer = layer_name

                # Add solid hatch
                hatch = modelspace.AddHatch(0, "SOLID", True)
                loop_array = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, [circle])
                hatch.AppendOuterLoop(loop_array)
                hatch.Evaluate()
                hatch.Layer = layer_name

            current_x += width + 10  # Move to next beam