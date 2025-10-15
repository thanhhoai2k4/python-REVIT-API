# -*- coding: utf-8 -*-
__title__ = "Create Door on Wall"

from Autodesk.Revit import DB
from Autodesk.Revit import UI
from Autodesk.Revit.DB import Structure
from Autodesk.Revit.UI import Selection

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Tạo một bộ lọc để chỉ cho phép chọn tường
class WallSelectionFilter(Selection.ISelectionFilter):
    def AllowElement(self, element):
        # Chỉ trả về True nếu đối tượng là một bức tường
        if isinstance(element, DB.Wall):
            return True
        return False

    def AllowReference(self, reference, point):
        return False

try:
    with DB.Transaction(doc, "Create Door") as t:
        t.Start()

        # Bước 1: Yêu cầu người dùng chọn một bức tường
        wall_filter = WallSelectionFilter()
        wall_ref = uidoc.Selection.PickObject(Selection.ObjectType.Element, wall_filter, "Hãy chọn một bức tường để đặt cửa")
        host_wall = doc.GetElement(wall_ref)

        # Bước 2: Tìm một loại cửa (FamilySymbol) trong dự án
        # Dùng FilteredElementCollector với danh mục là OST_Doors
        door_symbol = DB.FilteredElementCollector(doc)\
                        .OfCategory(DB.BuiltInCategory.OST_Doors)\
                        .WhereElementIsElementType()\
                        .FirstElement()

        if not door_symbol:
            UI.TaskDialog.Show("Lỗi", "Không tìm thấy loại cửa (Door Type) nào trong dự án. Hãy load một family cửa vào trước.")
            t.RollBack()
        else:
            # Kích hoạt family symbol nếu cần
            if not door_symbol.IsActive:
                door_symbol.Activate()
                doc.Regenerate()

            # Bước 3: Lấy các thông tin cần thiết từ tường vật chủ
            # Lấy level của tường
            level = doc.GetElement(host_wall.LevelId)
            
            # Lấy đường location của tường và tìm điểm giữa
            location_curve = host_wall.Location.Curve
            mid_point = location_curve.Evaluate(0.5, True) # 0.5 = 50% (điểm giữa), True = normalized

            # Bước 4: Tạo cửa bằng NewFamilyInstance
            # Sử dụng một overload khác của hàm này, có tham số 'host'
            new_door = doc.Create.NewFamilyInstance(
                mid_point,      # Vị trí đặt cửa trên tường
                door_symbol,    # Loại cửa (FamilySymbol)
                host_wall,      # Tường vật chủ (Host Element)
                level,          # Level chứa cửa
                Structure.StructuralType.NonStructural # Cửa không phải là đối tượng kết cấu
            )

            t.Commit()
            UI.TaskDialog.Show("Thành công", "Đã tạo cửa mới thành công!")

except Exception as e:
    if "Operation cancelled" in str(e):
        print("Thao tác đã bị hủy.")
    else:
        print("Đã xảy ra lỗi: {}".format(e))
    # Đảm bảo transaction được rollback nếu có lỗi
    if t.HasStarted() and not t.HasEnded():
        t.RollBack()