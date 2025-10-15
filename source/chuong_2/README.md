# REVIT và các yếu tố hình học


## Wall, Floors, Ceilings, Roofs and Openings

<pre>
    # Import các thư viện cần thiết
    from Autodesk.Revit.DB import Transaction, Wall, ElementId
    from Autodesk.Revit.UI.Selection import Selection

    # Lấy đối tượng tài liệu hiện hành
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument

    # Bắt đầu một Transaction
    t = Transaction(doc, "Create Walls")
    t.Start()

    try:
        # Lấy các đối tượng được chọn (các đường mô hình)
        # Bạn cần chọn các đường mô hình trước khi chạy script
        selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

        # Thay thế Wall Type ID và Level ID bằng các giá trị bạn đã ghi lại từ Revit Lookup
        # Ví dụ:
        wall_type_id = ElementId(310057) # Thay thế bằng Type ID của tường của bạn
        level_id = ElementId(310046) # Thay thế bằng Level ID của tầng của bạn

        # Lặp qua từng đối tượng được chọn
        for s in selection:
            # Chuyển đổi ModelLine thành GeometryCurve
            # Revit API cần Curve để tạo tường
            ln = s.GeometryCurve

            # Tạo tường
            # Các tham số:
            # doc: tài liệu Revit hiện hành
            # ln: đường cong (GeometryCurve)
            # wall_type_id: ElementId của loại tường
            # level_id: ElementId của tầng
            # height: Chiều cao của tường (ví dụ: 10 feet)
            # offset: Độ lệch của tường so với đường cong
            # flip: Boolean để lật hướng tường (False hoặc True)
            # structural: Boolean cho tường kết cấu (False hoặc True)
            Wall.Create(doc, ln, wall_type_id, level_id, 10, 0, False, False)

        # Commit Transaction để lưu các thay đổi
        t.Commit()
        print("Walls created successfully!")

    except Exception as ex:
        # Nếu có lỗi, rollback Transaction
        t.RollBack()
        print(f"Error: {ex}")

</pre>