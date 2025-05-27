import os
import json
import pythoncom
import win32com.client
from columns import draw_column_outline, draw_column_rebar
#from beams import draw_beam_outline, draw_beam_rebar


def get_acad_app():
    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
    except Exception:
        acad = win32com.client.Dispatch("AutoCAD.Application")
        acad.Visible = True
    return acad


def main():
    pythoncom.CoInitialize()
    acad = get_acad_app()

    base_dir = os.path.dirname(__file__)
    data_path = os.path.abspath(os.path.join(base_dir, "..", "data", "columns_data.json"))

    if not os.path.exists(data_path):
        print(f"ملف البيانات غير موجود: {data_path}")
        return

    with open(data_path, "r") as f:
        columns_data = json.load(f)
        # beams_data = json.load(f)

    draw_column_outline(acad, columns_data, layer_name="column_outline")
    draw_column_rebar(acad, columns_data, layer_name="column_rebar")

    # draw_beam_rebar(acad, beams_data, layer_name="beam_rebar")
    # draw_beam_outline(acad, beams_data, layer_name="beam_outline")


if __name__ == "__main__":
    main()
