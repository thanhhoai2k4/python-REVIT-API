# -*- coding: utf-8 -*-
__title__ = "show thuoc tinh cua 1 doi tuong"
__author__ = ""
__doc__ = """show thuoc tinh PT va ten cua 1 doi tuong"""

from Autodesk.Revit import DB
from Autodesk.Revit import UI


doc = __revit__.ActiveUIDocument.Document # everything revit has.
uidoc = __revit__.ActiveUIDocument  # everything you see.

if __name__ == '__main__':
    
    # cach chon 1 doi tuong
    selection = uidoc.Selection.PickObject(
        UI.Selection.ObjectType.Element,
        "Chon 1 doi tuong de xem tham so"
    )

    
    # # chon nhieu doi tuong
    # selectons = uidoc.Selection.PickObjects(
    #     UI.Selection.ObjectType.Element,
    #     "Chon nhieu doi tuong de xem tham so"
    # )

    element = doc.GetElement(selection.ElementId) # lay doi tuong tu id
    param_list = element.Parameters # lay danh sach tham so cua doi tuong

    print(type(element)) # in ra ten doi tuong
    for param in param_list:
        print("\t {0} : {1}".format(param.Definition.Name, param.AsValueString())) # in ra ten tham so va gia tri tham so
