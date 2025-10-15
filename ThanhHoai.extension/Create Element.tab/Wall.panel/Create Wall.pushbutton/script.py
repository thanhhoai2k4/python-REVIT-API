# -*- coding: utf-8 -*-
__title__ = "Create Wall"
__author__ = "Thanh Hoai"
__doc__ = """Day la nut de tao ra 1 tuong thang trong Revit voi chieu dai 50 feet va chieu cao 20 feet."""

from Autodesk.Revit.DB import Transaction # to make changes in Revit file
from Autodesk.Revit.DB import XYZ # to create points in 3D space
from Autodesk.Revit.DB import Line # to create lines

from Autodesk.Revit.DB import FilteredElementCollector # to collect elements in the project
from Autodesk.Revit.DB import WallType # to get wall types



# "------------"
from Autodesk.Revit.UI import TaskDialog as TD # to show a message box
from Autodesk.Revit import DB


uidoc = __revit__.ActiveUIDocument   # everthing you see.
doc = __revit__.ActiveUIDocument.Document # everything revit has.



"""
    public static Wall Create(
	    Document document,
	    IList<Curve> profile,
	    bool structural )
    
    document: is doc.
    profile: is a list of curves that make up the wall's location line.
    => class Curve: (Line, Arc, Ellipse, NurbSpline, HermiteSpline, PolyLine, etc...). 
    Line is the most common.
    create Line: Line.CreateBound(XYZ point1, XYZ point2)
    point1, point2: are two endpoints of the line.
    => class XYZ: represent a point in 3D space.
    XYZ point = new XYZ(double x, double y, double z) in c#;
    structural: is a bool value (True or False
)
"""



if __name__ == '__main__':
    
    with Transaction(doc, 'Create Wall') as t:
        t.Start()
        
        # create two points in 3D space
        start_point = XYZ(0, 0, 0)  # origin point
        end_point = XYZ(50, 0, 0)   # 10 feet along the X axis
        line = Line.CreateBound(start_point, end_point) # Create a Line between two points


        level = FilteredElementCollector(doc).OfClass(DB.Level).FirstElement() 
        # lay ra tat ca level trong project va lay level dau tien

        # kiem tra xem level no co ton tai hay khong
        if not level:
            TD.show("Error", "No wall type found in the project.")
            t.RollBack()
        else:
            # lay wall type dau tien trong project
            wall_type = FilteredElementCollector(doc).OfClass(WallType).FirstElement()
            if not wall_type:
                TD.show("Error", "No wall type found in the project.")
                t.RollBack()
            else:
                # set chieu cao
                wall_height = 20 # in feet

                # create wall
                new_wall = DB.Wall.Create(doc, line, wall_type.Id, level.Id, wall_height, 0, False, False)
                # DB.Wall.Create(document, profile, wallTypeId, levelId, height, offset, structural, flip)

                TD.Show("Success", "Wall created successfully.")

        
        t.Commit()