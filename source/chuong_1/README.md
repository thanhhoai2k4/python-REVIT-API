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

