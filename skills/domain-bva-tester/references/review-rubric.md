# Rubric Đánh Giá, Chấm Điểm & Refactor Test Case EShop

Tài liệu dùng cho chế độ **Review** (chấm điểm test case của sinh viên / AI sinh ra), **Refactor** (chuẩn hóa test case cũ/lộn xộn sang template chuẩn), và tự kiểm tra (Self-check) trước khi bàn giao.

---

## 1. Thang Điểm 0–2 Cho 7 Thuộc Tính Chất Lượng (Tổng /14 Điểm)

| Thuộc tính | 2 Điểm (Đạt chuẩn) | 1 Điểm (Đạt một phần) | 0 Điểm (Không đạt) |
|---|---|---|---|
| **Accurate** | Các bước và kết quả mong đợi khớp 100% mục tiêu tại tiêu đề | Có 1 chi tiết nhỏ hơi lệch mục tiêu nhưng không phá hỏng test case | Tiêu đề và nội dung test hai chức năng hoàn toàn khác nhau |
| **Economical** | Chỉ chứa các bước cần thiết để kiểm chứng mục tiêu | Có 1–2 bước rườm rà lặp lại không đáng kể | Gộp 3-4 mục tiêu lớn vào một case; lặp lại luồng thiết lập dài dòng |
| **Repeatable** | Dữ liệu kiểm thử cụ thể (giá trị số/chuỗi rõ ràng), ai chạy cũng ra cùng kết quả | Dữ liệu tương đối rõ nhưng còn 1 chỗ để tester tự quyết định | Dùng từ chung chung: "nhập mật khẩu hợp lệ", "chọn vài sản phẩm" |
| **Traceable** | Ánh xạ chính xác tới mã yêu cầu tồn tại thật (`FR-01`..`FR-24`, `SEC-xx`) | Có nhắc đến yêu cầu nhưng viết tên mơ hồ, không gắn mã chuẩn | Không có mã yêu cầu hoặc gán mã bịa đặt không có trong spec |
| **Appropriate** | Môi trường, công cụ, quyền hạn phù hợp với hiện trạng SUT EShop | Thiếu thông tin môi trường thực thi chi tiết | Nhầm lẫn giữa quyền Admin và User, hoặc áp đặt công cụ không phù hợp |
| **Self-standing** | Test case độc lập hoàn toàn, tự cung cấp đủ dữ liệu và tiền điều kiện | Còn một giả định ngầm nhỏ về trạng thái dữ liệu | Phụ thuộc vào kết quả của test case khác ("dùng tài khoản vừa tạo ở TC-01") |
| **Self-cleaning** | Có bước hoàn tác/xóa dữ liệu sau khi chạy, hoặc không làm biến đổi CSDL | Có ý thức dọn dẹp nhưng bước thực hiện chưa triệt để | Tạo user, đơn hàng, coupon nhưng bỏ mặc làm bẩn môi trường test |

### Kết luận đánh giá (Verdict):
- **Accept (Chấp nhận)**: Tổng điểm $\ge 12/14$ và không có lỗi mức High.
- **Revise (Cần sửa đổi)**: Tổng điểm từ $8 - 11/14$, hoặc có lỗi mức High nhưng có thể sửa được.
- **Reject (Bác bỏ)**: Tổng điểm $< 8/14$, hoặc kết quả mong đợi bịa đặt sai lệch nghiêm trọng so với đặc tả EShop SUT, hoặc trùng lặp hoàn toàn với case khác.

---

## 2. Danh Mục Phân Loại Lỗi (Defect Taxonomy)

Khi ghi nhận lỗi của test case, bắt buộc sử dụng các nhãn danh mục chuẩn sau:

| Nhãn danh mục (Category) | Dấu hiệu nhận diện | Mức độ nghiêm trọng |
|---|---|---|
| **Wrong expected result** | Kết quả mong đợi mâu thuẫn trực tiếp với đặc tả EShop (ví dụ: spec ghi khóa 30s sau 3 lần nhưng test case ghi sau 5 lần) | **High** |
| **Fuzzy verdict** | Dùng từ phán quyết mơ hồ: "hoạt động bình thường", "hiển thị đúng", "như mong đợi" | **High** |
| **Missing expected result** | Các bước hành động nhưng không có phản hồi hệ thống tương ứng | **High** |
| **Vague test data** | Không cung cấp giá trị dữ liệu cụ thể (ví dụ: "nhập coupon hợp lệ") | **High** |
| **Missing step** | Thiếu bước kích hoạt then chốt (ví dụ: nhập mã nhưng không bấm nút "Áp dụng") | **High** |
| **Broken setup** | Tiền điều kiện không khả thi hoặc thiếu tài khoản cần thiết | **Medium** |
| **Too long / multi-objective** | Quá 15 bước hoặc gom nhiều luồng nghiệp vụ khác nhau vào 1 case | **Medium** |
| **Stale / invented UI** | Tên nút, nhãn trường không có trên giao diện thực tế của EShop | **Medium** |
| **No cleanup** | Ghi dữ liệu vào CSDL nhưng không có bước dọn dẹp môi trường sạch | **Medium** |
| **Unclear actor** | Dùng câu bị động, không phân biệt tester làm hay hệ thống phản hồi | **Low** |
| **Redundant** | Trùng phân hoạch tương đương với một test case đã có | **Low** |
| **Not traceable** | Không có mã yêu cầu nghiệp vụ để truy vết | **Low** |
| **Bad title** | Tiêu đề không tuân theo quy tắc Action + Function + Condition | **Low** |

---

## 3. Quy Trình Đối Chiếu Review Do AI Sinh Ra (AI Review Audit)

Khi thực hiện bài tập theo yêu cầu HW02, sinh viên phải kiểm chứng lại các nhận xét do AI đưa ra và lập bảng đối chiếu 3 nhóm:
1. **Confirmed (Lỗi xác nhận)**: Lỗi do AI chỉ ra và bạn đã xác minh là có thật trên test case hoặc trên SUT EShop (kèm bằng chứng cụ thể: file, dòng code, mã test case).
2. **False Positives (AI báo sai)**: Điểm AI báo là lỗi nhưng thực chất lại đúng theo đặc tả EShop (kèm lý do phân tích tại sao AI hiểu nhầm).
3. **Missed (AI bỏ sót)**: Lỗi nghiệp vụ hoặc lỗi logic thực tế mà AI không phát hiện ra (giải thích nguyên nhân: do prompt chưa đủ chi tiết hay giới hạn mô hình).

---

## 4. Quy Trình Refactor Test Case Cũ Sang Chuẩn EShop

1. **Trích xuất mục tiêu**: Đọc bản test case cũ (dạng văn xuôi, checklist sơ sài), xác định các mục tiêu kiểm thử riêng biệt.
2. **Tách và đánh mã**: Mỗi mục tiêu trở thành một test case độc lập với mã `TC-<PHÂN_HỆ>-<SỐ>` duy nhất.
3. **Chuẩn hóa Anatomy**:
   - Viết lại tiêu đề theo cấu trúc `Action + Function + Condition`.
   - Bổ sung tiền điều kiện chính xác về tài khoản và trạng thái CSDL.
   - Viết từng bước hành động ở thể chủ động kèm phản hồi mong đợi có thể quan sát.
   - Bổ sung giá trị dữ liệu cụ thể (BVA/EP).
   - Thêm bước dọn dẹp (`cleanup`).
4. **Đối chiếu đặc tả**: Kiểm tra lại toàn bộ kết quả mong đợi với tài liệu `README.md` của EShop.
5. **Ghi nhận ánh xạ**: Điền vào bảng `refactor.mapping` (bản cũ -> mã mới -> thay đổi cụ thể).
