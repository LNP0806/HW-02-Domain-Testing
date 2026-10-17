---
name: eshop-test-case-writing
description: Thiết kế, chuẩn hóa, tổ chức và xuất tài liệu test case chuẩn quốc tế (anatomy đầy đủ, tiêu đề Action + Function + Condition, step-by-step hoặc data matrix, 7 thuộc tính chất lượng, rubric review 0-2) dành riêng cho hệ thống EShop (React Web storefront, React Admin, React Native Expo Mobile, Node Express Backend, SQLite). Áp dụng phương pháp Kiểm thử Miền (Domain Testing / Equivalence Partitioning) và Phân tích Giá trị Biên (BVA 2-value / 3-value), bảng quyết định (Decision Table) và máy trạng thái (State Machine) cho 4 phân hệ (Pool A Auth/Catalog, Pool B Cart/Checkout/Coupon, Pool C Web Admin CRUD/CSV, Pool D Mobile). Hỗ trợ 3 chế độ (Thiết kế mới từ đặc tả EShop, Refactor test case cũ lộn xộn, Review/Audit test case của AI hoặc sinh viên). Kiểm tra tính hợp lệ bằng linter và tự động xuất đồng thời file Word (.docx) và Excel (.xlsx) có ma trận truy vết, dropdown trạng thái, công thức đếm tự động COUNTIF và nhật ký AI Audit Report.
---

# Kỹ Năng Thiết Kế & Soạn Thảo Test Case Cho Hệ Thống EShop (Word + Excel)

Skill này hướng dẫn quy trình kiểm thử toàn diện, có phương pháp luận và chuẩn mực cao cho hệ sinh thái **EShop SUT** (`https://github.com/ttbhanh/eshop-sut`). Toàn bộ quy trình kết hợp lý thuyết kiểm thử phần mềm chính thống (Kaner, IEEE Std 729, Myers, ISTQB Foundation Level) với bộ công cụ tự động hóa xuất bản Word và Excel đồng bộ.

Mọi bộ test case đều được định nghĩa qua **một file JSON chuẩn duy nhất** (`references/json-schema.md`) → kiểm tra tĩnh bằng `scripts/lint_testcases.py` → xuất bản đồng thời tài liệu **Word (.docx)** và bảng tính **Excel (.xlsx)** bằng `scripts/build_testcase_docs.py`.

---

## Bước 0 — Xác Định Chế Độ Làm Việc & Phân Hệ EShop

### 1. Chọn chế độ làm việc

| Người dùng yêu cầu... | Chế độ thực thi | Nhiệm vụ chính |
|---|---|---|
| Đưa yêu cầu chức năng (FR-xx), tài liệu đặc tả, hoặc yêu cầu kiểm thử 1 tính năng EShop | **Thiết kế (Design)** | Bóc tách biến miền, xác định phân hoạch VEC/IEC, lập BVA 2-value/3-value, sinh bộ test case hoàn chỉnh |
| Đưa file test case cũ (văn xuôi, thiếu trường, sơ sài) và bảo "chuẩn hóa / làm lại cho chuẩn" | **Refactor** | Tách mục tiêu, chuẩn hóa anatomy, đối chiếu đặc tả EShop, điền bảng `refactor.mapping` |
| Đưa bộ test case có sẵn (của sinh viên hoặc AI khác sinh ra) và bảo "chấm điểm / review" | **Review & Audit** | Chấm 0–2 điểm trên 7 thuộc tính (/14), dán nhãn lỗi chuẩn, đối chiếu `review.ai_review_check` |

### 2. Xác định phân hệ (Pool) và tính năng theo đặc tả HW02

> [!IMPORTANT]
> **4 Tính Năng Trọng Tâm Được Chọn Cho Bài Tập HW02 (Zero Duplication Scope):**
> 1. **Pool A:** **FR-06 — Xem chi tiết sản phẩm (Product Detail View)**
> 2. **Pool B:** **FR-11 — Xem lịch sử đơn hàng người dùng (Order History View)**
> 3. **Pool C:** **FR-15 — Quản lý sản phẩm CRUD Web Admin (Product CRUD)**
> 4. **Pool D:** **Lịch sử đơn hàng trên Ứng dụng Di Động (Mobile Order History)**
>
> *(Xem bộ test case mẫu đầy đủ 20 test cases tại `assets/selected-4-features-testcases.json`)*

- **Pool A (Authentication, Categories & Products)**: FR-01 (Đăng ký), FR-02 (Đăng nhập & Khóa 30s), FR-03 (Quên/Đặt lại mật khẩu OTP 2 bước), FR-04 (Hồ sơ cá nhân), FR-05 (Tìm kiếm SP), **FR-06 (Chi tiết SP - Chọn)**.
- **Pool B (Shopping Cart & Checkout)**: FR-07 (Giỏ hàng), FR-08 (Thanh toán & Tính lại tiền trên server), FR-09 (Mã giảm giá 5 điều kiện C1..C5), FR-10 (Máy trạng thái đơn hàng), **FR-11 (Lịch sử đơn - Chọn)**.
- **Pool C (Web Admin)**: FR-12 (Kiểm soát quyền role admin), FR-13 (Dashboard doanh thu đơn delivered), FR-14 (Danh mục), **FR-15 (CRUD Sản phẩm - Chọn)**, FR-16 (Import CSV nguyên tử All-or-Nothing), FR-17 (CRUD Coupon), FR-18 (Admin quản lý đơn), FR-19 (Admin quản lý user).
- **Pool D (Mobile App)**: **Lịch sử đơn hàng trên Mobile App (Chọn)** — Đánh giá trong bối cảnh thiết bị di động (ngắt mạng/timeout, thiếu pull-to-refresh, Safe Area notch, đối chiếu ẩn nút hủy).
- **GUI & Bảo mật**: FR-21 đến FR-24; SEC-01 đến SEC-07.

---

## Bước 1 — Hiểu Rõ Đặc Tả SUT & Bóc Tách Biến Miền

1. Đọc kỹ `references/eshop-spec-guide.md` để nắm chắc logic nghiệp vụ, bảng CSDL SQLite, tài khoản mẫu và các endpoint API.
2. **Liệt kê chính xác tên trường, nút bấm và thông báo lỗi trên giao diện thực tế**:
   - Mở file `.jsx` tương ứng trong `eshop-sut/frontend-web/src/pages/` hoặc `frontend-admin/src/` để lấy đúng text (ví dụ: nút bấm là "Đăng Ký", "Đăng nhập", "Áp dụng", "Thanh toán"). Tránh lỗi AI bịa tên nút (stale UI).
3. **Bóc tách biến đầu vào**:
   - Biến số (số tiền, số lượng, số lần sai, số điện thoại, độ dài mật khẩu).
   - Biến chuỗi / định dạng (email, format mật khẩu, mã coupon, file CSV).
   - Biến thời gian / trạng thái (hạn coupon, trạng thái đơn hàng, quyền role JWT).
4. **Ghi nhận giả định**: Nếu có điểm đặc tả chưa nói rõ, ghi tường minh vào `meta.assumptions`.

---

## Bước 2 — Thiết Kế Phân Hoạch Tương Đương & Phân Tích Giá Trị Biên

Thực hiện theo tài liệu phương pháp luận `references/domain-bva-methodology.md`:

1. **Phân hoạch tương đương (Equivalence Partitioning)**:
   - Xác định rõ các lớp hợp lệ (Valid Equivalence Classes - VEC) và lớp không hợp lệ (Invalid Equivalence Classes - IEC).
   - Đảm bảo mỗi lớp không hợp lệ được kiểm tra trong một test case độc lập (nguyên tắc cách ly lỗi).
2. **Phân tích giá trị biên (Boundary Value Analysis)**:
   - Áp dụng phương pháp **3-value BVA** cho các ngưỡng số học và độ dài: `Boundary - 1`, `Boundary`, `Boundary + 1`.
   - Các ngưỡng biên trọng yếu của EShop:
     - Độ dài mật khẩu: `7` (fail), `8` (pass), `9` (pass).
     - Số lần đăng nhập sai: `2` (chưa khóa), `3` (kích hoạt khóa 30s), `4` (chặn ngay lập tức).
     - Ngưỡng đơn hàng SAVE10 (300.000 ₫): `299.999 ₫` (fail), `300.000 ₫` (pass), `300.001 ₫` (pass).
     - Hạn dùng coupon: `expired_at - 1 ngày` (pass), `expired_at` (fail).
     - Lượt dùng mã: `used = 0` (pass), `used = max_uses` (fail).
     - Số lượng sản phẩm: `0` (fail), `1` (pass), `2` (pass).
     - Giá sản phẩm: `0 ₫` (fail), `1 ₫` (pass).
3. **Bảng quyết định & Máy trạng thái**:
   - Dùng Bảng quyết định (Decision Table) cho các tính năng đa điều kiện như FR-09 (Coupon 5 điều kiện).
   - Dùng Ma trận chuyển đổi trạng thái (State Transition Matrix) cho FR-10 (Đơn hàng 5 trạng thái).

---

## Bước 3 — Soạn Thảo Test Case Chuẩn Anatomy EShop

### 1. Cú pháp Tiêu đề (Mandatory)
Phải tuân thủ nghiêm ngặt công thức: **ACTION + FUNCTION + CONDITION**
- *Đúng:* "Kiểm tra áp dụng mã SAVE10 khi tổng đơn hàng vừa đủ ngưỡng 300.000 ₫"
- *Đúng:* "Xác minh từ chối đăng ký tài khoản khi mật khẩu chỉ dài 7 ký tự (thiếu 1 ký tự)"
- *Sai:* "Test coupon" hoặc "Kiểm tra chức năng đăng ký hoạt động tốt"

### 2. Chọn định dạng Suite
- **Định dạng Ma trận dữ liệu (`format: "matrix"`)**: Thích hợp cho các ca kiểm thử BVA và EP có cùng quy trình thao tác (ví dụ: ma trận kiểm tra mật khẩu, ma trận biên ngưỡng coupon). Viết quy trình `procedure` 1 lần, mỗi dòng có `covers` ghi rõ lớp biên.
- **Định dạng Từng bước (`format: "steps"`)**: Thích hợp cho hành trình giao diện (UI User Flow), luồng qua nhiều trang (ví dụ: luồng đặt hàng, chuyển trạng thái đơn hàng). Mỗi bước có `action` và phản hồi hệ thống `expected` (tối đa 15 bước).

### 3. Đạt đủ 7 thuộc tính chất lượng
- **Accurate**: Test đúng mục tiêu ở tiêu đề.
- **Economical**: Không có bước thừa.
- **Repeatable**: Dữ liệu cụ thể, số tiền cụ thể, tài khoản cụ thể.
- **Traceable**: Gắn mã yêu cầu `FR-01`..`FR-24`, `SEC-01`..`SEC-07`.
- **Appropriate**: Phù hợp môi trường SUT EShop.
- **Self-standing**: Độc lập, không phụ thuộc vào kết quả của test case khác.
- **Self-cleaning**: Có bước `cleanup` dọn dẹp dữ liệu (xóa user, xóa đơn hàng trong SQLite).

---

## Bước 4 — Kiểm Tra Tĩnh (Lint) & Tự Động Xuất Bản Tài Liệu

### 1. Chạy linter kiểm tra file JSON:
```bash
python skills/eshop-test-case-writing/scripts/lint_testcases.py <đường_dẫn_file.json>
```
- Linter sẽ tự động phát hiện: ID sai định dạng, tiêu đề thiếu Action/Condition, từ ngữ mơ hồ ("hoạt động tốt", "đúng như mong đợi"), câu bị động, số bước > 15, thiếu dọn dẹp dữ liệu, test case trùng lặp hoặc yêu cầu chưa được bao phủ.
- **Yêu cầu:** Sửa sạch 100% các thông báo `[ERROR]`; rà soát các cảnh báo `[WARN]`.

### 2. Biên dịch xuất đồng thời Word (.docx) và Excel (.xlsx):
```bash
python skills/eshop-test-case-writing/scripts/build_testcase_docs.py <đường_dẫn_file.json> --out-dir <thư_mục_xuất> --basename <Tên_Tài_Liệu>
```
- **Word (.docx)**: Trình bày chuẩn A4 dọc gồm Thông tin tài liệu, Giới thiệu, Ma trận truy vết yêu cầu, Bảng tổng hợp test case, Chi tiết từng test case (dạng bảng template step-by-step hoặc ma trận dữ liệu), Bảng Review/Chấm điểm, Bảng Refactor Mapping và Khai báo AI Audit.
- **Excel (.xlsx)**: Gồm Sheet `Tổng quan` (tự động đếm thống kê trạng thái bằng công thức COUNTIF), Sheet `Test Cases` (đầy đủ các bước, dropdown chọn trạng thái Pass/Fail/Blocked tô màu tự động, cố định dòng tiêu đề, bộ lọc Filter), các Sheet Ma trận dữ liệu riêng biệt, Sheet `Truy vết` (đánh dấu cảnh báo đỏ nếu yêu cầu chưa có test case bao phủ), Sheet `Review` và Sheet `Checklist`.

---

## Bước 5 — Bàn Giao, Đối Chiếu Bug Thực Tế & Lập AI Audit Log

1. **Đối chiếu Bug trên SUT EShop**:
   - Cho biết kết quả kỳ vọng theo đặc tả lý thuyết đối lập với hành vi lỗi trong source code thực tế (ví dụ: Regex mật khẩu sai kiểm tra khoảng trắng trong `Register.jsx`, ô tổng tiền cho phép sửa trong `Checkout.jsx`, API Admin thiếu middleware kiểm tra role, v.v.).
2. **Chuẩn bị dữ liệu cho AI Audit Report**:
   - Ghi lại Prompt đầu vào, thời gian tương tác, mô hình sử dụng và các chỉnh sửa con người đã can thiệp vào file JSON / tài liệu kiểm thử.
3. **Phản hồi người dùng ngắn gọn**:
   - Tóm tắt tổng số test case, tỷ lệ bao phủ yêu cầu, danh sách giả định, đường dẫn file Word và Excel đã tạo. Tuyệt đối không paste lại toàn bộ nội dung test case vào khung chat vì đã có tài liệu hoàn chỉnh.

---

## Tài Nguyên & Tham Khảo

- `references/eshop-spec-guide.md` — Toàn bộ kiến trúc, CSDL SQLite, tài khoản, endpoint API và các lỗi tiềm ẩn của EShop SUT.
- `references/domain-bva-methodology.md` — Phương pháp kiểm thử miền, phân hoạch EP, kỹ thuật BVA 2-value/3-value, bảng quyết định và heuristic mobile.
- `references/test-case-guide.md` — Quy chuẩn soạn thảo test case, anatomy, 7 thuộc tính chất lượng và cạm bẫy AI.
- `references/review-rubric.md` — Thang chấm điểm 0–2 (/14), danh mục phân loại lỗi và quy trình review/refactor.
- `references/json-schema.md` — Đặc tả cấu trúc JSON làm nguồn cấp dữ liệu cho linter và bộ sinh tài liệu.
- `assets/example-eshop-coupon.json` — Bộ test mẫu hoàn chỉnh cho Pool B: FR-08 & FR-09 (Mã giảm giá & Thanh toán).
- `assets/example-eshop-auth.json` — Bộ test mẫu hoàn chỉnh cho Pool A: FR-01 & FR-02 (Đăng ký, Đăng nhập & Khóa tài khoản).
- `scripts/lint_testcases.py` — Script kiểm tra tĩnh chất lượng test case theo quy chuẩn EShop.
- `scripts/build_testcase_docs.py` — Script tự động xuất bản đồng thời tài liệu Word (.docx) và Excel (.xlsx).
