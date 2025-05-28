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
        
    def APoint(self, *args):
        """
        Creates a VARIANT-compatible 3D point (or 2D point with Z=0) 
        for use with AutoCAD COM methods.

        Parameters:
            x, y, z (float)
            (x, y, z) (tuple) 
            [x, y, z] (list)
            
            Examples:
            APoint(10, 20)
            APoint(10, 20, 30)
            APoint((10, 20))
            APoint([10, 20, 30])

        Returns:
            win32com.client.VARIANT: A VARIANT containing a VT_ARRAY of VT_R8 (doubles)
            representing the point [x, y, z].

        Notes:
            - This format is required for AutoCAD methods like AddLine, AddCircle, AddPolyline, etc.
            - For 2D operations, you can omit the Z-coordinate; it will default to 0.
        """
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            coords = args[0]
        else:
            coords = args

        if len(coords) < 2 or len(coords) > 3:
            raise ValueError("APoint requires 2 or 3 coordinates (x, y[, z])")

        x = float(coords[0])
        y = float(coords[1])
        z = float(coords[2]) if len(coords) == 3 else 0.0
        
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))

    def ADouble(self, points: list[float] | tuple[float]):
        """
        Converts a sequence of real numbers (float) into a VARIANT array of doubles (R8) 
        for use with AutoCAD COM methods.

        Parameters:
            points (list or tuple of float): A flat list or tuple of real numbers representing 
            coordinates or numeric values, typically used for points (e.g., [x, y, z]).

        Returns:
            win32com.client.VARIANT: A VARIANT containing a VT_ARRAY of VT_R8 (double) values,
            suitable for AutoCAD COM methods that require ADouble inputs (e.g., AddLine, AddCircle).

        Notes:
            - This is required because AutoCAD COM expects certain arguments (like points or dimensions)
            as arrays of doubles, not plain Python lists or tuples.
            - The input must be a flat sequence of float numbers (not nested lists).
        """
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, points)

    def variants(self, objects):
        """
        Converts one or more COM objects into a VARIANT array of dispatch types 
        for use with AutoCAD COM methods that expect this format.

        Parameters:
            objects (object or list of objects): A single COM object or a list/tuple of 
                COM objects (e.g., AutoCAD entities like lines, circles, or other entities) 
                to be wrapped.

        Returns:
            win32com.client.VARIANT: A VARIANT containing a VT_ARRAY of VT_DISPATCH 
                objects, suitable for passing to AutoCAD COM methods that require this 
                specific format, such as `Group.AppendItems()` or `Hatch.AppendOuterLoop()`.

        Notes:
            - AutoCAD COM methods typically do not accept native Python lists or tuples 
            directly; this method wraps the provided objects into a VARIANT array 
            with the correct type for AutoCAD.
            - If a single object is provided, it will be wrapped as a one-element array 
            (i.e., still in tuple form).
            - This is primarily used for methods like `AppendOuterLoop()`, `AppendInnerLoop()`, 
            or other AutoCAD API calls that expect arrays of dispatch objects.
        """
        if not isinstance(objects, (list, tuple)):  
            objects = [objects]
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, tuple(objects))

    def add_layer(self, name, color=7, linetype="Continuous", lineweight=-3, description=""):
        """
        Add or get an AutoCAD layer.

        Args:
            name (str): Name of the layer.
            color (int): AutoCAD color number (1-256). Default is 7 (white).
            linetype (str): Linetype name (e.g., "Continuous").
            lineweight (int): Lineweight enum. Default -1 (Default).
            description (str): Layer description Default ""

        Returns:
            COM Layer object.
        """
        layers = self.doc.Layers
        try:
            layer = layers.Item(name)
            print(f"Layer {name} already exist!") # GUI_MSG
        except Exception:
            layer = layers.Add(name)
            print(f"Layer {name} created.") # GUI_MSG

            layer.Color = color
        
            if self.add_linetype(linetype):
                layer.Linetype = linetype
        
            if lineweight != -3:
                layer.Lineweight = lineweight
                
            if description:
                layer.Description = description
                
        return layer
    
    def add_linetype(self, linetype="Continuous"):
        try:
            if linetype not in self.get_existing_linetypes():
                self.doc.Linetypes.Load(linetype, "acad.lin")
                return True
        except Exception as e:
            print(f"Failed to load linetype '{linetype}': {e}.") # GUI_MSG
            return False
        return True
    
    def get_existing_linetypes(self) -> list[str]:
        """ 
        Get the linetypes existing in the document.

        Returns:
            list[str]: List of the linetypes existing in the document.
        """
        linetype = self.doc.Linetypes
        return [lt.name for lt in linetype]

    def add_line(self, start: tuple[int | float | int, float], end: tuple[int | float | int, float], layer=None):
        """
        Draw a line in model space.

        Args:
            start (tuple): Start point (x, y, z).
            end (tuple): End point (x, y, z).
            layer (str): Layer name to assign.

        Returns:
            COM Line object.
        """
        line = self.model_space.AddLine(self.APoint(start), self.APoint(end))
        if layer:
            line.Layer = layer
        return line

    def add_circle(self, center: tuple[int | float | int, float], radius: float, layer=None):
        """
        Draw a circle in model space.

        Args:
            center (tuple): Center point (x, y, z).
            radius (float): Radius of the circle.
            layer (str): Layer name to assign.

        Returns:
            COM Circle object.
        """
        circle = self.model_space.AddCircle(self.APoint(center), radius)
        if layer:
            circle.Layer = layer
        return circle

    def add_lightweight_polyline(self, coords: list[float] | tuple[float], layer=None):
        """
        Draw a lightweight polyline using coordinate list.

        Args:
            coords (list | tuble): List or tuble of (x1, y1, x2, y2, ..., xn, yn) coordinates.
            layer (str): Layer name to assign.

        Returns:
            COM Polyline object.
        """
        polyline = self.model_space.AddLightWeightPolyline(self.ADouble(coords))
        if layer:
            polyline.Layer = layer
        return polyline

    def add_hatch(self,pattern_type=0, pattern_name="SOLID", associative=True):
        """
        Create a new hatch object.
        
         - Pattren Types:
            * 0: Predefined patterns (like "SOLID", "ANSI31", etc.)
            * 1: User-defined patterns (simple lines)
            * 2: Custom patterns from a .pat file.
         - Pattren Names:
            * You can find it in AutoCAD
         - Associativity (Associativity=False in AddHatch): If you set Associativity to True, the hatch will remain linked to its boundary, (e.g. If you modify the circle later, the hatch will update automatically). If False, it's a static hatch

        Args:
            pattern_type (int): Hatch pattern type. Default is 0.
            pattern_name (str): Hatch pattern name. Default is "SOLID".
            associative (bool): Whether the hatch is associative.

        Returns:
            COM Hatch object.
        """
        return self.model_space.AddHatch(pattern_type, pattern_name, associative)

    def append_outer_loop(self, object, hatch_object):
        """
        Append an outer boundary loop to a hatch object.

        Parameters:
            object (object or list of objects): The boundary entity or entities 
                (e.g., lines, arcs, polylines) that form the outer loop of the hatch.
            hatch_object (win32com.client.CDispatch): The AutoCAD Hatch object 
                to which the outer loop will be appended.

        Note:
            This typically defines the main closed region that will be filled by the hatch.
            The input object(s) must already exist in the drawing and form a closed loop.
        """
        hatch_object.AppendOuterLoop(self.variants(object))

    def append_inner_loop(self, object, hatch_object):
        """
        Append an inner boundary loop (a hole or exclusion) to a hatch object.

        Parameters:
            object (object or list of objects): The boundary entity or entities 
                (e.g., lines, arcs, polylines) that form the inner loop.
            hatch_object (win32com.client.CDispatch): The AutoCAD Hatch object 
                to which the inner loop will be appended.

        Note:
            Inner loops define areas within the hatch boundary that will remain unhatched.
            Useful for creating islands or holes inside a hatched region.
        """
        hatch_object.AppendinnerLoop(self.variants(object))
        
