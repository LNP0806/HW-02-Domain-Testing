# Hướng Dẫn Soạn Thảo Test Case Chuẩn Mực Cho EShop

Tài liệu hướng dẫn chuẩn hóa cú pháp, cấu trúc và văn phong trình bày test case cho hệ thống **EShop**, tuân thủ các nguyên tắc từ bài giảng "Writing Effective Test Cases — AI-First" (Kaner, IEEE 729, Runnels).

---

## 1. Nguyên Tắc Cốt Lõi

> **Mỗi Test Case = Một Mục Tiêu Kiểm Thử + Dữ Liệu Cụ Thể + Kết Quả Mong Đợi Đo Lường Được.**

- **Tính tái lập (Reproducibility)**: Bất kỳ thành viên nào trong nhóm hoặc người chấm bài đọc test case đều có thể thực thi chính xác và đạt cùng một kết luận Pass/Fail.
- **Tính tự chứng (Self-verifiable)**: Không chấp nhận các kết quả mơ hồ như "hệ thống chạy tốt", "hiển thị đúng", "như mong đợi".

---

## 2. Cấu Trúc Đầy Đủ Của Một Test Case EShop (Anatomy)

Một test case chuẩn mực bao gồm 3 nhóm thông tin chính:

| Nhóm | Trường thông tin | Quy ước cho EShop | Ví dụ cụ thể |
|---|---|---|---|
| **Định danh** | **Mã Test Case (ID)** | `TC-<PHÂN_HỆ>-<SỐ>` | `TC-AUTH-001`, `TC-COUPON-003`, `TC-ADMIN-PROD-010` |
| | **Tiêu đề (Title)** | Action + Function + Condition | "Kiểm tra áp dụng mã SAVE10 khi tổng giỏ hàng đạt 300.000 ₫" |
| | **Mục đích (Purpose)** | 1 câu gắn liền với mã yêu cầu | "Xác nhận yêu cầu FR-09: hệ thống chiết khấu 10% khi đơn đủ ngưỡng." |
| | **Mã yêu cầu (Traceability)**| Danh sách mã FR-xx hoặc SEC-xx | `["FR-09", "FR-08"]` |
| | **Độ ưu tiên (Priority)** | `High` \| `Medium` \| `Low` | `High` cho luồng nghiệp vụ chính và thanh toán |
| | **Loại (Type)** | `Positive` \| `Negative` \| `Boundary` \| `Security` | `Boundary` cho kiểm thử biên giá trị |
| **Thực thi** | **Thiết lập / Tiền điều kiện** | Môi trường, trạng thái tài khoản, CSDL | "Đã đăng nhập tài khoản test@eshop.com; giỏ hàng có 1 SP giá 300.000 ₫" |
| | **Dữ liệu kiểm thử (Test Data)**| Giá trị đầu vào cụ thể | `code: "SAVE10", total_amount: 300000, user_id: 2` |
| | **Các bước thực hiện (Steps)** | Câu chủ động, chủ thể rõ ràng (≤ 15 bước) | 1. Tại trang Checkout, nhập mã SAVE10 vào ô "Mã giảm giá"<br>2. Nhấn nút "Áp dụng" |
| **Kết quả** | **Kết quả mong đợi (Expected)**| Trạng thái có thể quan sát, đo lường được | "Hiển thị thông báo 'Áp dụng mã thành công'; dòng Giảm giá hiển thị -30.000 ₫; Tổng tiền thanh toán cập nhật thành 270.000 ₫" |
| | **Dọn dẹp (Self-cleaning)** | Trả môi trường về trạng thái sạch | "Xóa đơn hàng vừa tạo trong SQLite hoặc làm mới giỏ hàng" |
| | **Trạng thái thực thi** | `Not run` \| `Pass` \| `Fail` \| `Blocked` | Cập nhật khi chạy thực tế trên hệ thống SUT |

---

## 3. Cú Pháp Tiêu Đề: ACTION + FUNCTION + CONDITION

Tiêu đề là phần quan trọng nhất khi tổng hợp báo cáo và truy vết:
- **ACTION**: Động từ hành động (Kiểm tra / Xác minh / Xác nhận / Validate / Verify / Test).
- **FUNCTION**: Tên chức năng hoặc màn hình đang kiểm thử.
- **CONDITION**: Điều kiện môi trường, trạng thái người dùng hoặc dữ liệu biên cụ thể.

**Các ví dụ chuẩn:**
- `TC-AUTH-002`: "Kiểm tra khóa tài khoản tạm thời 30 giây khi người dùng nhập sai mật khẩu 3 lần liên tiếp"
- `TC-COUPON-005`: "Xác minh từ chối mã giảm giá SAVE10 khi tổng giá trị đơn hàng chỉ đạt 299.999 ₫ (dưới ngưỡng tối thiểu)"
- `TC-ADMIN-CSV-003`: "Kiểm tra cơ chế rollback giao dịch nguyên tử khi import file CSV có dòng thứ 3 sai định dạng giá"
- `TC-MOB-CART-004`: "Kiểm tra hiển thị nút Đặt hàng trên Mobile khi mở bàn phím ảo điền địa chỉ giao hàng"

---

## 4. Lựa Chọn Định Dạng: Step-by-Step hay Data Matrix?

### Định dạng 1: Step-by-step (`format: "steps"`)
- **Dùng khi**: Hành trình người dùng (User Journey), luồng qua nhiều màn hình (UI flow), quy trình nghiệp vụ phức tạp.
- **Đặc trưng**: Mỗi bước là 1 cặp `action` (hành động người dùng) và `expected` (phản hồi quan sát được từ hệ thống).
- **Ví dụ**: Đăng ký tài khoản (FR-01), Đặt hàng và thanh toán (FR-08), Chuyển trạng thái đơn hàng (FR-10).

### Định dạng 2: Data Matrix (`format: "matrix"`)
- **Dùng khi**: Cùng một quy trình thao tác giống hệt nhau, chỉ có bộ dữ liệu đầu vào và kết quả thay đổi.
- **Đặc trưng**: Quy trình chung (`procedure`) được viết một lần duy nhất. Bảng gồm các cột đầu vào, kết quả mong đợi và cột `covers` chỉ rõ lớp phân hoạch hoặc giá trị biên tương ứng.
- **Ví dụ**:
  - Ma trận kiểm thử sức mạnh mật khẩu (FR-01).
  - Ma trận các tổ hợp điều kiện mã giảm giá (FR-09).
  - Ma trận định dạng số điện thoại trong hồ sơ (FR-04).
  - Ma trận import CSV sản phẩm (FR-16).

---

## 5. Bảy Thuộc Tính Của Test Case Tốt (Rubric Chấm Điểm)

1. **Accurate (Chính xác)**: Test case tập trung đúng vào mục tiêu nêu ở tiêu đề, không đi lạc sang kiểm tra những chức năng khác.
2. **Economical (Tiết kiệm)**: Tinh gọn, không chứa thao tác thừa (ví dụ không lặp lại bước đăng nhập 20 lần trong một ma trận test).
3. **Repeatable (Tái lập được)**: Luôn đi kèm dữ liệu cụ thể (giá trị số, chuỗi ký tự chính xác), bất kỳ tester nào chạy lại cũng ra cùng kết quả.
4. **Traceable (Truy vết được)**: Ánh xạ trực tiếp về mã yêu cầu cụ thể (`FR-01` đến `FR-24`, `SEC-01` đến `SEC-07`).
5. **Appropriate (Phù hợp)**: Phù hợp với năng lực kiểm thử, công cụ (Postman/Trình duyệt/Mobile Emulator) và môi trường SUT.
6. **Self-standing (Độc lập)**: Tự cung tự cấp dữ liệu, không ngầm giả định "dùng kết quả của test case trước".
7. **Self-cleaning (Tự dọn dẹp)**: Mọi thao tác ghi dữ liệu (tạo user, tạo đơn, tạo coupon) đều có bước hoàn tác hoặc xóa để không làm sai lệch các lần chạy sau.

---

## 6. Lỗi Thường Gặp & Cạm Bẫy Của AI Sinh Test Case

Khi sử dụng AI để sinh test case cho EShop, đặc biệt lưu ý kiểm tra các lỗi sau:

| Lỗi phổ biến | Biểu hiện trên EShop | Cách khắc phục |
|---|---|---|
| **1. Bịa kết quả mong đợi (Hallucination)** | AI tự suy đoán mã lỗi hoặc cách ứng xử mà spec không nêu (ví dụ: đoán mã giảm giá được cộng dồn). | Luôn đối chiếu với bảng đặc tả `README.md` của EShop SUT. |
| **2. Bịa tên nút / Nhãn giao diện (Stale UI)** | AI viết "Bấm nút Tiếp Tục" hoặc "Bấm Submit" trong khi UI thực tế là nút "Thanh toán" hoặc "Sign In". | Xem trực tiếp source code Frontend (`.jsx`) để lấy đúng text hiển thị trên nút. |
| **3. Phán quyết mơ hồ (Fuzzy Verdict)** | Kết quả ghi: "Hệ thống hoạt động đúng", "Giao diện hiển thị phù hợp". | Phải chỉ rõ: Xuất hiện Toast thông báo "...", nút bị disable, trường `total_amount` chuyển thành 270.000 ₫. |
| **4. Thiếu bước hành động (Missing Step)** | Nhập dữ liệu xong nhưng không ghi bước bấm nút Submit / Áp dụng. | Mỗi test case phải có hành động kích hoạt sự kiện rõ ràng. |
| **5. Không dọn dẹp dữ liệu (No Cleanup)** | Chạy test case đăng ký user thành công nhưng không xóa, khiến lần chạy sau bị lỗi "Email đã tồn tại". | Bổ sung bước xóa user trong SQLite hoặc đặt email có tiền tố timestamp/ngẫu nhiên. |
