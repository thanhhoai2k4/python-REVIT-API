# 1. Cấu trúc của một extention

# 1.1 Nền tản lý thuyết về Database và User Interface trong REVIT API
Thông thường thì các API của Pyrevit sẽ được nằm ở Autodesk.
<pre>
    import Autodek
    print(dir(Autodek))
    output: ['Revit']
</pre>
output: là 1 danh sách bao gồm 1 phần tử. Nới đây chứa tất cả các API để tương tác với REVIT.

Và trong Autodesk.Revit chứa các Class:
<pre>
    from Autodesk import Revit
    print(dir(Revit))
    output: ['ApplicationServices', 'Attributes', 'Creation', 'DB', 'Exceptions', 'UI']
</pre>

Giải thích về các class này: 
- tao 1 cái bản
- có 6 dòng và 1 cột
- giải thích các class này

VD:

| Cột 1 | Cột 2 | Cột 3 |
|-------|--------|-------|
| Hàng 1 - A | Hàng 1 - B | Hàng 1 - C |
| Hàng 2 - A | Hàng 2 - B | Hàng 2 - C |



Document(doc): đây là đối tượng đại diện cho cơ sở dử liệu. Nó chứa tất cả các Element(Tường, cửa, ...) các cài đặt, thông tin dự án. Mọi thao tác <b>truy vấn</b> và <b>lọc</b> đều thông qua đối tượng này.

UIDocument(uidoc): Đại diện cho lớp giao diện người dùng mà chúng ta đang tương tác. Nó quản lý những gì mà chúng ta thấy trên màn hình, cửa sổ và đặt biệt là các hành động lựa chọn đối tượng.


## Filtering

Công cụ chính cho việc này là FilteredElementCollector. <br>
Cách hoạt động: Bạn bắt đầu một FilteredElementCollector, sau đó áp dụng các bộ lọc (OfCategory, OfClass, WhereElementIsNotElementType, etc.) để thu hẹp phạm vi tìm kiếm.
<pre>
    # Import các thư viện cần thiết
    from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Wall

    # Lấy document hiện hành
    doc = __revit__.ActiveUIDocument.Document

    # Bắt đầu Collector, lọc theo category là Walls và lấy về các element instances
    walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

    # In ra số lượng tường tìm thấy
    print("Tìm thấy {} bức tường.".format(len(walls)))

    for wall in walls:
        # wall bây giờ là một đối tượng Wall, bạn có thể truy cập thuộc tính của nó
        print("ID của tường: {}".format(wall.Id))
</pre>



## Selection

Đây là cách để bạn tương tác với những gì người dùng đang chọn trực tiếp trên giao diện Revit. <br>
Cách hoạt động: Bạn truy cập vào UIDocument (giao diện người dùng) để lấy tập hợp các đối tượng đang được chọn.
<pre>
    from Autodesk.Revit.DB import ElementId

    # Lấy uidoc (tài liệu giao diện người dùng)
    uidoc = __revit__.ActiveUIDocument

    # Lấy tập hợp các ID của element đang được chọn
    selected_ids = uidoc.Selection.GetElementIds()

    if not selected_ids:
        print("Không có đối tượng nào được chọn.")
    else:
        print("Các đối tượng đang được chọn:")
        for element_id in selected_ids:
            # Từ ID, ta có thể lấy về đối tượng Element
            element = doc.GetElement(element_id)
            print("- ID: {}, Category: {}".format(element.Id, element.Category.Name))
</pre>

## Parameters

<pre>
    # Giả sử 'wall' là một đối tượng tường đã được lấy từ trước
    # (ví dụ: wall = walls[0] từ mục Filtering)

    # Lấy parameter bằng tên
    comment_param = wall.LookupParameter("Comments")

    if comment_param:
        # Đọc giá trị cũ
        old_comment = comment_param.AsString()
        print("Comment cũ: '{}'".format(old_comment))
        
        # Ghi giá trị mới (phải nằm trong Transaction)
        # Xem mục 7. Transactions
        from Autodesk.Revit.DB import Transaction
        
        t = Transaction(doc, "Thay đổi Comment của tường")
        t.Start()
        
        comment_param.Set("Đây là comment mới từ script Python")
        
        t.Commit()
        
        print("Đã cập nhật comment thành công.")

</pre>

## Collections

😅🤣☺️


##  Views

<pre>

    from Autodesk.Revit.DB import Transaction

    # Lấy view đang mở
    active_view = doc.ActiveView

    print("Tên view hiện tại: {}".format(active_view.Name))

    # Đổi tên view
    t = Transaction(doc, "Đổi tên View")
    t.Start()

    active_view.Name = active_view.Name + " - Đã chỉnh sửa"

    t.Commit()

    print("Đã đổi tên view thành công.")

</pre>


## Transactions 

Transaction đảm bảo tính toàn vẹn của cơ sở dữ liệu. Nó cho phép Revit "gom" một loạt các thay đổi lại thành một hành động duy nhất. Nếu có lỗi xảy ra giữa chừng, toàn bộ các thay đổi trong transaction sẽ được hoàn tác (rollback), giữ cho mô hình không bị hỏng. Nó cũng là cơ chế để Revit có thể thực hiện chức năng Undo/Redo.