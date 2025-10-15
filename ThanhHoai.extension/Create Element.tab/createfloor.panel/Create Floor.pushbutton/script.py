# -*- coding: utf-8 -*-
__title__ = "Create Floor"
__author__ = "Thanh Hoai"
__doc__ = """This is Hello World Button.
Click on it see what happens..."""

from System.Collections.Generic import List
from Autodesk.Revit import DB
from Autodesk.Revit import UI

uidoc = __revit__.ActiveUIDocument  # everything you see.
doc = __revit__.ActiveUIDocument.Document # everything revit has.





if __name__ == '__main__':
    
    with DB.Transaction(doc, 'Hello World') as t:
        t.Start()
        
        # tim level 
        level = DB.FilteredElementCollector(doc).OfClass(DB.Level).FirstElement() 

        # tim floor type
        floor_type = DB.FilteredElementCollector(doc)\
                        .OfCategory(DB.BuiltInCategory.OST_Floors)\
                        .WhereElementIsElementType()\
                        .FirstElement()

        if not level or not floor_type:
            UI.TaskDialog.Show('Error', 'No level or floor type found in this project.')
            t.RollBack()
        else:
            p1 = DB.XYZ(0, 0, 0)
            p2 = DB.XYZ(10 * 3.28084, 0, 0)        # 10m theo trục X
            p3 = DB.XYZ(10 * 3.28084, 5 * 3.28084, 0) # 5m theo trục Y
            p4 = DB.XYZ(0, 5 * 3.28084, 0)  

            # tao cac duong Line
            line1 = DB.Line.CreateBound(p1, p2)
            line2 = DB.Line.CreateBound(p2, p3)
            line3 = DB.Line.CreateBound(p3, p4)
            line4 = DB.Line.CreateBound(p4, p1)
            
            # tao cac duong cong khep kin
            curve_loop = DB.CurveLoop()
            curve_loop.Append(line1)
            curve_loop.Append(line2)
            curve_loop.Append(line3)
            curve_loop.Append(line4)

            list_of_curve_loops = List[DB.CurveLoop]([curve_loop])
            # tao san
            # Bước 6: Tạo sàn (SỬA LẠI DÒNG NÀY)
            new_floor = DB.Floor.Create(
                doc,                   # 1. Document
                list_of_curve_loops,   # 2. IList<CurveLoop>
                floor_type.Id,         # 3. ElementId của FloorType
                level.Id               # 4. ElementId của Level
            )
            
            UI.TaskDialog.Show("Thành công", "Đã tạo sàn mới thành công!")

        t.Commit()