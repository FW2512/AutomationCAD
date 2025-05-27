import pythoncom
import win32com.client


class AutoCADController:
    """
    A class to manage the AutoCAD COM interface using pythoncom and win32com.

    Provides methods to:
    - Connect to AutoCAD
    - Access model space
    - Add layers, lines, circles, polylines, and hatches
    """

    def __init__(self):
        """
        Initialize the COM connection with AutoCAD and get the active document and model space.
        """
        pythoncom.CoInitialize()
        try:
            self.acad = win32com.client.GetActiveObject("AutoCAD.Application")
        except Exception:
            self.acad = win32com.client.Dispatch("AutoCAD.Application")

        self.acad.Visible = True
        self.doc = self.acad.ActiveDocument
        self.model_space = self.doc.ModelSpace

    def add_layer(self, name, color=7, linetype="Continuous", lineweight=-1):
        """
        Add or get an AutoCAD layer.

        Args:
            name (str): Name of the layer.
            color (int): AutoCAD color number (1-256). Default is 7 (white).
            linetype (str): Linetype name (e.g., "Continuous").
            lineweight (int): Lineweight enum. Default -1 (ByLayer).

        Returns:
            COM Layer object.
        """
        layers = self.doc.Layers
        try:
            layer = layers.Item(name)
        except Exception:
            layer = layers.Add(name)

        layer.Color = color
        layer.Linetype = linetype
        if lineweight != -1:
            layer.Lineweight = lineweight
        return layer

    def add_line(self, start, end, layer=None):
        """
        Draw a line in model space.

        Args:
            start (tuple): Start point (x, y, z).
            end (tuple): End point (x, y, z).
            layer (str): Layer name to assign.

        Returns:
            COM Line object.
        """
        line = self.model_space.AddLine(start, end)
        if layer:
            line.Layer = layer
        return line

    def add_circle(self, center, radius, layer=None):
        """
        Draw a circle in model space.

        Args:
            center (tuple): Center point (x, y, z).
            radius (float): Radius of the circle.
            layer (str): Layer name to assign.

        Returns:
            COM Circle object.
        """
        circle = self.model_space.AddCircle(center, radius)
        if layer:
            circle.Layer = layer
        return circle

    def add_lightweight_polyline(self, coords, layer=None):
        """
        Draw a lightweight polyline using coordinate list.

        Args:
            coords (list): List of [x1, y1, x2, y2, ..., xn, yn] coordinates.
            layer (str): Layer name to assign.

        Returns:
            COM Polyline object.
        """
        import array
        polyline = self.model_space.AddLightWeightPolyline(array.array("d", coords))
        if layer:
            polyline.Layer = layer
        return polyline

    def add_hatch(self, pattern="SOLID", associative=True):
        """
        Create a new hatch object.

        Args:
            pattern (str): Hatch pattern name. Default is "SOLID".
            associative (bool): Whether the hatch is associative.

        Returns:
            COM Hatch object.
        """
        return self.model_space.AddHatch(0, pattern, associative)
