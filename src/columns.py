import pythoncom
import win32com.client


def draw_column_outline(acad, columns_data, layer_name="column_outline"):
    doc = acad.ActiveDocument
    model = doc.ModelSpace

    try:
        doc.Layers.Item(layer_name)
    except:
        doc.Layers.Add(layer_name)

    for column_name, floors in columns_data.items():
        floor1 = floors.get("floor1")
        if not floor1:
            continue

        dims = floor1.get("dimensions")
        if not dims:
            continue

        width = dims.get("width_x", 0)
        height = dims.get("height_y", 0)

        points = [
            0, 0, 0,
            width, 0, 0,
            width, height, 0,
            0, height, 0,
            0, 0, 0
        ]

        variant_points = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_R8,
            points
        )

        poly = model.AddPolyline(variant_points)
        poly.Layer = layer_name

def draw_column_rebar(acad, columns_data, layer_name="column_rebar"):
    doc = acad.ActiveDocument
    model = doc.ModelSpace

    try:
        doc.Layers.Item(layer_name)
    except:
        doc.Layers.Add(layer_name)

    doc.ActiveLayer = doc.Layers.Item(layer_name)

    for column_name, floors in columns_data.items():
        for floor_name, floor_data in floors.items():
            dims = floor_data.get("dimensions", {})
            rebars = floor_data.get("rebars", {})
            cover = dims.get("cover", 5)
            width = dims.get("width_x", 0)
            height = dims.get("height_y", 0)

            corners = [
                (cover, cover),
                (width - cover, cover),
                (width - cover, height - cover),
                (cover, height - cover)
            ]

            for x, y in corners:
                point = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [x, y, 0])
                model.AddCircle(point, 1.5)

            if "middle" in rebars:
                mid_x = width / 2
                mid_y = height / 2
                for mx, my in [(mid_x, cover), (mid_x, height - cover), (cover, mid_y), (width - cover, mid_y)]:
                    point = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [mx, my, 0])
                    model.AddCircle(point, 1.5)