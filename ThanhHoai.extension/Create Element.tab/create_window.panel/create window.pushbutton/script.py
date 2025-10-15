# -*- coding: utf-8 -*-
__title__ = "Create Window on Wall"

from Autodesk.Revit import DB
from Autodesk.Revit import UI
from Autodesk.Revit.DB import Structure
from Autodesk.Revit.UI import Selection

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

# Bộ lọc để chỉ cho phép chọn Tường (giữ nguyên như cũ)
class WallSelectionFilter(Selection.ISelectionFilter):
    def AllowElement(self, element):
        if isinstance(element, DB.Wall):
            return True
        return False
    def AllowReference(self, reference, point):
        return False

try:
    with DB.Transaction(doc, "Create Window") as t:
        t.Start()

        # Bước 1: Yêu cầu người dùng chọn một bức tường vật chủ
        wall_filter = WallSelectionFilter()
        wall_ref = uidoc.Selection.PickObject(Selection.ObjectType.Element, wall_filter, "Hãy chọn một bức tường để đặt cửa sổ")
        host_wall = doc.GetElement(wall_ref)

        # Bước 2: Tìm một loại cửa sổ (FamilySymbol) trong dự án
        # THAY ĐỔI CHÍNH: Dùng BuiltInCategory.OST_Windows thay vì OST_Doors
        window_symbol = DB.FilteredElementCollector(doc)\
                          .OfCategory(DB.BuiltInCategory.OST_Windows)\
                          .WhereElementIsElementType()\
                          .FirstElement()

        if not window_symbol:
            UI.TaskDialog.Show("Lỗi", "Không tìm thấy loại cửa sổ (Window Type) nào trong dự án. Hãy load một family cửa sổ vào trước.")
            t.RollBack()
        else:
            # Kích hoạt family symbol nếu cần
            if not window_symbol.IsActive:
                window_symbol.Activate()
                doc.Regenerate()

            # Bước 3: Lấy level và tính toán vị trí đặt cửa sổ
            level = doc.GetElement(host_wall.LevelId)
            location_curve = host_wall.Location.Curve
            mid_point = location_curve.Evaluate(0.5, True)

            # Bước 4: Tạo cửa sổ bằng NewFamilyInstance
            new_window = doc.Create.NewFamilyInstance(
                mid_point,
                window_symbol,
                host_wall,
                # Level không cần thiết trong overload này, Revit tự lấy từ tường
                # Tuy nhiên, một số overload khác sẽ cần nó.
                Structure.StructuralType.NonStructural
            )
            
            # Bước 5 (Thêm): Điều chỉnh chiều cao bệ cửa (Sill Height)
            # Lấy tham số Sill Height bằng BuiltInParameter
            sill_height_param = new_window.get_Parameter(DB.BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM)
            
            # Gán chiều cao mới là 900mm (nhớ đổi sang feet)
            height_in_mm = 900
            height_in_feet = height_in_mm / 304.8
            sill_height_param.Set(height_in_feet)

            t.Commit()
            UI.TaskDialog.Show("Thành công", "Đã tạo cửa sổ mới với bệ cửa cao 900mm!")

except Exception as e:
    if "Operation cancelled" in str(e):
        print("Thao tác đã bị hủy.")
    else:
        print("Đã xảy ra lỗi: {}".format(e))
    if t.HasStarted() and not t.HasEnded():
        t.RollBack()