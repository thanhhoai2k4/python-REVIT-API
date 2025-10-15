# -*- coding: utf-8 -*-
__title__ = "Hello World"
__author__ = ""
__doc__ = """This is Hello World Button.
Click on it see what happens..."""

from Autodesk.Revit import DB
from Autodesk.Revit import UI

uidoc = __revit__.ActiveUIDocument  # everything you see.
doc = __revit__.ActiveUIDocument.Document # everything revit has.

if __name__ == '__main__':

    with DB.Transaction(doc, 'Hello World') as t:
        
        t.Start()

        # viet code o day.
        level = DB.FilteredElementCollector(doc).OfClass(DB.Level).FirstElement()
        if not level:
            UI.TaskDialog.Show('Error', 'No level found in this project.')
            t.RollBack()
        else:
            column_symbol = DB.FilteredElementCollector(doc)\
                       .OfCategory(DB.BuiltInCategory.OST_StructuralColumns)\
                       .WhereElementIsElementType()\
                       .FirstElement()
            
            if not column_symbol:
                UI.TaskDialog.Show('Error', 'No column type found in this project.')
                t.RollBack()
            else:
                if column_symbol.IsActive == False:
                    column_symbol.Activate()
                    doc.Regenerate()
                
                # tao vi tri de dat cot
                point = DB.XYZ(0, 0, 0) # toa do diem (0,0,0)
                column = doc.Create.NewFamilyInstance(
                    point, # vi tri ma cot no 
                    column_symbol, # kieu cot
                    level, # level ma cot no nam tren do
                    DB.Structure.StructuralType.Column # kieu cau truc la cot
                )

                UI.TaskDialog.Show('Success', 'Column created successfully.')

                # thay doi chieu cao cua cot
                column.LookupParameter('Top Offset').Set(50) # 20 feet to meters
                

        t.Commit()