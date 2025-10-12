# python-REVIT-API
Đây là 1 project để tôi có thể lưu trữ các đoạn mả và giải thích về các API của REVIT được viết.

Tài liệu và file:
 - [REVIT 2026](https://drive.google.com/file/d/1Sa2_jeIE9PyUkd2nIdfET08NyOALSWCo/view): đây là phiên bản mới nhất hiện nay (pass: <b>vietcons.org</b>)
 - [ pyRevit 5.2.0.25181 Installer](https://github.com/pyrevitlabs/pyRevit/releases/download/v5.2.0.25181%2B1332/pyRevit_5.2.0.25181_admin_signed.exe): Phiên bản Pyrevit mới nhất dành cho nhà phát triển.
 - [API REVIT 2026](https://www.revitapidocs.com/2026/): đây là nơi tra cứu các class chính trong REVIT API.
- [REVIT API Developers Guide](https://help.autodesk.com/view/RVT/2024/ENU/?guid=Revit_API_Revit_API_Developers_Guide_html): code mẫu C# của [Autodesk](https://help.autodesk.com/view/RVT/2024/ENU/).

# Tổng quan về Python trong REVIT

Autodesk cung cấp 1 bộ API để python có thể tương tác với ngôn ngữ c# cực kì mạnh mẻ. C# là 1 ngôn ngữ có cấu trúc rất phức tạm:
- Hiểu cách tham chiếu đến các thư viện.
- Phải khai báo tường minh các biến.
- Biên dịch chương trình sang file .dll mỏi khi có sự thay đổi nhỏ.

    
Python là một món mì ăn liền <3. Khi chúng ta có sự thay đổi nhỏ thì chỉ cần reload lại trong Pyrevit. Diển ra tức thì. Ngôn ngữ gần gủi con người, ngắn gọn.


So sánh về hiệu năng: </br>
+ C#:  có tốc độ vược trộ vì được biên dịch sang mã máy.
+ Python: chậm và chậm. Vì có 1 lớp trung gian dịch. Vì thế chậm =)). Tuy nhiên với tác vụ cơ bản(quản lý tham số, tên, lấy dữ liệu,...) thì sẽ không nhận ra bằng mắt thường.

<div style="display: flex; justify-content: space-between;">

  <div style="width: 48%;">
    <h3>Python</h3>
    <p>
        Nên sử dụng cho nhưng tác vụ cơ bản.
    </p>
  </div>

  <div style="width: 48%;">
    <h3>C#</h3>
    <p>
        Khi hiệu năng là trên hết.
    </p>
  </div>

</div>


# Bài học

## [1. Tương tác cơ bản với phần tử REVIT](source/chuong_1/README.md)
 - [Filtering](source/chuong_1/README.md#filtering)
 - [Selection](source/chuong_1/README.md#Selection)
 - [Parameters](source/chuong_1/README.md#Parameters)
 - [Collections](source/chuong_1/README.md#Collections)
 - [Views](source/chuong_1/README.md#Parameters)
 - [Transactions](source/chuong_1/README.md#Parameters)