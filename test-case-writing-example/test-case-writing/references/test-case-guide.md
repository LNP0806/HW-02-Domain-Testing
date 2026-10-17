# Hướng dẫn viết và trình bày test case

Nguồn: bài giảng "Writing Effective Test Cases — AI-First" (FIT, VNUHCM-US), dựa trên Kaner–Falk–Nguyen (*Testing Computer Software*), IEEE Std 729, Dianne L. Runnels (*How to Write Better Test Cases*), QATutor Lecture 3. Ví dụ xuyên suốt: chương trình Tam giác (Myers, 1979).

## Mục lục
1. Định nghĩa và quy tắc gốc
2. Cấu trúc (anatomy) của một test case
3. Cú pháp tiêu đề: Action + Function + Condition
4. Ba định dạng — chọn cái nào
5. Ngôn ngữ và độ dài (testability)
6. Bảy thuộc tính của test case tốt
7. Năm tiêu chí "xuất sắc" (Kaner)
8. Dấu hiệu test case yếu
9. Bảy lỗi phổ biến nhất
10. Lỗi đặc trưng khi AI sinh test case
11. Checklist review
12. Tổ chức bộ test (suite), đánh số, thứ tự

---

## 1. Định nghĩa và quy tắc gốc

- Kaner: "Một test (lý tưởng) thực thi **một** mục tiêu kiểm thử được xác định rõ."
- IEEE 729: "Một tập dữ liệu test cụ thể và các thủ tục đi kèm, được xây dựng cho một mục tiêu cụ thể."

**Quy tắc ngón tay cái: một test case = một mục tiêu + dữ liệu cụ thể + kết quả mong đợi tường minh, kiểm chứng được.**

Vì sao phải viết test case: tìm lỗi; tái lập (ai cũng chạy lại được); trách nhiệm giải trình (bằng chứng đã test gì); theo dõi tiến độ/số liệu; tự động hoá (test case viết rõ là một script đang chờ); xác nhận việc thực thi đúng; tuân thủ (audit); đo độ bao phủ.

## 2. Cấu trúc (anatomy)

| Nhóm | Trường | Ghi chú |
|---|---|---|
| **Định danh** | Mã test case & tên | TC-<MÔĐUN>-<NN>, vd TC-LOGIN-003 |
| | Tiêu đề / mục tiêu (1 dòng) | Theo cú pháp mục 3 |
| | Mục đích — yêu cầu được truy vết | vd "SRS-4.2: hệ thống phải chặn thông tin đăng nhập sai và báo lỗi" |
| | Người viết, phiên bản, môi trường | |
| **Thực thi** | Thiết lập & tiền điều kiện | môi trường, dữ liệu, quyền truy cập, trạng thái ban đầu |
| | Các bước — hành động + phản hồi hệ thống | mỗi bước có kết quả mong đợi |
| | Dữ liệu test / tham số / đầu vào | giá trị cụ thể |
| | Phương pháp: thủ công, ma trận, script | |
| **Kết quả** | Kết quả mong đợi — **phải viết ra!** | |
| | Kết quả thực tế | điền khi chạy |
| | Trạng thái: Pass / Fail / Blocked / Skipped | (+ Not run khi chưa chạy) |
| | Mã lỗi, bằng chứng, ghi chú | |

Tiêu đề một dòng thường là phần **duy nhất** được ghi lại — hãy làm cho nó đáng giá.

### Template tối thiểu, đã điền

| Trường | Nội dung |
|---|---|
| ID / Title | TC-LOGIN-003 — Verify login is rejected with a valid username and wrong password |
| Purpose | Requirement SRS-4.2: system must block invalid credentials and show an error |
| Setup | User account student01 exists; browser at login page; test DB restored |
| Steps | 1. Enter username student01  2. Enter password wrongpass!  3. Click Log in |
| Expected result | Error "Invalid username or password" shown; user stays on login page; no session created |
| Status / Bug ID | Pass ☐ Fail ☐ Blocked ☐   Bug: ____ |

"No session created" kiểm chứng được — "login should not work" thì không.

## 3. Cú pháp tiêu đề: ACTION + FUNCTION + CONDITION

- **ACTION**: Verify · Test · Validate · Calculate · Print · Run (tiếng Việt: Kiểm tra · Xác minh · Xác nhận · Tính · In · Chạy)
- **FUNCTION**: chức năng hoặc điểm kiểm tra
- **CONDITION**: điều kiện vận hành hoặc dữ liệu

Ví dụ:
- Verify login with valid username and wrong password
- Validate triangle classification when all three sides are equal
- Test Draw! button when one side field is left blank
- Kiểm tra phân loại tam giác khi ba cạnh bằng nhau (4, 4, 4)

Tiêu đề tốt giúp review, bàn giao và tự động hoá dễ hơn. Đưa dữ liệu đại diện vào ngoặc khi nó làm rõ điều kiện.

## 4. Ba định dạng — một anatomy

| Định dạng | Mô tả | Dùng khi |
|---|---|---|
| **Step-by-step** | Các bước đánh số: hành động + kết quả mong đợi | Luồng nghiệp vụ, hành trình UI, ít biến |
| **Data matrix** | Một bảng; mỗi dòng = dữ liệu + kết quả của một test case | Quy trình lặp lại, chỉ dữ liệu thay đổi (vd ô chuyển đổi tiền tệ, Tam giác) |
| **Automated script** | Code / record-playback; comment mang mục đích, đầu vào, kết quả | Regression, hiệu năng |

Dù định dạng nào, anatomy giữ nguyên. Ma trận vẫn cần: quy trình chung được viết ra một lần, tiền điều kiện, mã + (lý tưởng) tiêu đề cho mỗi dòng, cột "Bao phủ" (covers) cho biết dòng đó nhắm lớp/biên nào, và truy vết.

Ví dụ step-by-step (TC-TRI-01 — Verify classification and drawing with a scalene input (6, 5, 3)):

| # | Action | Expected result |
|---|---|---|
| 1 | Open the Triangle page in Chrome | Page loads; three empty side fields and Draw! visible |
| 2 | Enter 6, 5, 3 into Side 1, Side 2, Side 3 | Values shown in the fields exactly as typed |
| 3 | Click Draw! | Label "SCALENE" is displayed and a triangle is drawn fully inside the grey box |

Ví dụ data matrix:

| Side 1 | Side 2 | Side 3 | Expected output | Covers |
|---|---|---|---|---|
| 3 | 4 | 5 | Right-angled | valid class |
| 4 | 4 | 4 | Equilateral | valid class |
| 3 | 3 | 10 | Invalid — inequality fails | boundary logic |
| 0 | 5 | 5 | Invalid — zero side | boundary value |
| 1 | 1 | asd | Invalid input message | bad type |
| 2 | — blank — | 3 | Invalid input message | missing value |

## 5. Ngôn ngữ và độ dài (testability)

**Ngôn ngữ**
- Câu chủ động: "nhập…", "nhấn…", "hệ thống hiển thị…"
- Từ ngữ đơn giản, tự nhiên
- Tên trường chính xác và nhất quán — đúng như trên giao diện ("Side 1", "Draw!"), không bao giờ "cái ô", "nút kia"
- Không giải thích kiến thức cơ bản về hệ điều hành/trình duyệt

**Độ dài & thứ tự**
- ≤ 10–15 bước (trừ khi công việc không thể lưu giữa chừng)
- Thời gian chạy giữa các case tương đối đồng đều; ma trận chạy ≤ 20 phút
- Viết sao cho nhiều trình độ tester đều chạy được
- Sắp xếp case theo kịch bản nghiệp vụ thực tế

Testability = dễ test. Nếu tester mới còn lưỡng lự, cần sửa test case — không phải tester.

## 6. Bảy thuộc tính của test case tốt (rubric chấm)

| Thuộc tính | Ý nghĩa | Ví dụ vi phạm/đạt |
|---|---|---|
| **Accurate** (chính xác) | Test đúng điều tiêu đề nói | Tiêu đề "phân loại" → bước không lan sang kiểm tra kích thước canvas |
| **Economical** (tiết kiệm) | Không bước thừa | Không mở lại trình duyệt cho mỗi dòng trong 20 dòng ma trận |
| **Repeatable** (lặp lại được) | Ai chạy, lúc nào cũng ra cùng kết quả | "nhập 6, 5, 3" — không bao giờ "nhập vài số hợp lệ" |
| **Traceable** (truy vết được) | Ánh xạ về yêu cầu | TC-TRI-05 ← SRS-3.2 "từ chối cạnh bằng 0 hoặc âm" |
| **Appropriate** (phù hợp) | Hợp môi trường và đội tester | Không viết Selenium cho đội chỉ test thủ công |
| **Self-standing** (độc lập) | Không phụ thuộc người viết, không "kiến thức ngầm" | Không có "dùng dữ liệu từ test trước của tôi" |
| **Self-cleaning** (tự dọn dẹp) | Trả môi trường về trạng thái sạch | Bước 7 xoá tài khoản tạo ở bước 1 |

## 7. Năm tiêu chí "xuất sắc" (Kaner)

1. **Xác suất bắt lỗi hợp lý** — nhắm vào lỗi có thể xảy ra. vd 3,4,5 → "Right"; lỗi khả dĩ là gán nhầm "Scalene".
2. **Không quá đơn giản, không quá phức tạp** — case quá tải che giấu nguyên nhân. vd phân loại + vẽ + 3 trình duyệt trong một case: phần nào hỏng?
3. **Không trùng lặp** — mỗi case phải xứng đáng có mặt. vd 5,6,10 và 6,7,11 cùng một phân hoạch → giữ một.
4. **Tốt nhất trong loại** — chọn ứng viên mạnh nhất. vd biên trên: cạnh = 999 999 999 lộ lỗi nhiều hơn cạnh = 100.
5. **Làm lỗi lộ rõ** — không tranh cãi pass/fail. vd mong đợi "nhãn SCALENE xuất hiện", không phải "tam giác hiển thị đúng".

## 8. Dấu hiệu test case yếu

- **Xấu:** "Check that search works properly." → **Tốt hơn:** "Verify search shows 'No results found' for the query zzqx9 (zero matches)."
- Để tester tự nghĩ dữ liệu ("nhập ba cạnh hợp lệ" — cạnh nào?)
- Chỉ dẫn chung chung, mở cho "diễn giải nghệ thuật" ("test chức năng vẽ thật kỹ")
- Bỏ qua trình độ người chạy (giả định tester biết "tam giác suy biến" là gì)
- Thiếu bước xác minh — Pass/Fail thành ý kiến cá nhân ("nhấn Draw!" … rồi sao?)

## 9. Bảy lỗi phổ biến nhất

| # | Lỗi | Ví dụ |
|---|---|---|
| 1 | Quá dài | 25 bước: đăng ký → đăng nhập → vẽ → xuất, tất cả trong một case |
| 2 | Thiết lập hỏng | Giả định tài khoản student01 tồn tại — thực ra không |
| 3 | Thiếu bước | Kiểm tra nhãn nhưng không bao giờ bảo nhấn Draw! |
| 4 | Tên cũ (stale) | Bước ghi "Submit" — nút giờ là "Draw!" |
| 5 | Chủ thể mơ hồ | "giá trị được nhập" — tester hay hệ thống? |
| 6 | Phán quyết mờ | Kết quả mong đợi: "tam giác trông đúng" |
| 7 | Không dọn dẹp | Dữ liệu test được lưu làm hỏng lần chạy sau |

AI cũng mắc nhiều lỗi này — đặc biệt #4, #6, #7.

## 10. Lỗi đặc trưng khi AI sinh test case

- **Kết quả mong đợi bịa (hallucinated)** — tự tin, cụ thể… và sai. vd AI nói 1,1,2 là "Isosceles" — thực ra Invalid.
- **Trùng lặp trông hợp lý** — mười case cùng một happy path, số khác nhau cho có.
- **Thiếu biên miền** — cạnh số thực, giá trị rất lớn, hình vẽ tràn canvas; AI bỏ qua những gì spec không nói rõ.
- **Bịa giao diện/trường** — bước nhắc tới nút/thông báo không tồn tại.

Quy tắc nhà: **không test case nào do AI sinh được vào bộ test cho đến khi con người kiểm chứng kết quả mong đợi với spec.**

Mẫu prompt (ROLE · CONTEXT · TASK · FORMAT · CONSTRAINTS): "Bạn là QA engineer cao cấp. Đây là spec: <dán spec>. Viết 10 test case bao phủ đầu vào hợp lệ, không hợp lệ, biên. Bảng: ID | Title | Steps | Data | Expected result. Tiêu đề theo Action + Function + Condition; ≤ 15 bước; mỗi bước có phản hồi mong đợi." Sau đó hỏi tiếp "Bạn còn bỏ sót đầu vào nào?".

## 11. Checklist review

1. Đạt 7 thuộc tính: chính xác, tiết kiệm, lặp lại được, truy vết được, phù hợp, độc lập, tự dọn dẹp
2. Có mã/tên và mục đích gắn với yêu cầu
3. Mô tả thiết lập: môi trường, dữ liệu, tiền điều kiện, quyền truy cập
4. Mọi hành động có kết quả mong đợi; ghi bằng chứng khi cần
5. Câu chủ động; ≤ 15 bước; ma trận chạy ≤ 20 phút
6. Đúng thứ tự kịch bản nghiệp vụ so với các test khác
7. Theo quy ước đặt tên/đánh số; có phiên bản tương ứng phần mềm được test
8. Lưu trữ có kiểm soát truy cập và sao lưu (quản lý cấu hình)

## 12. Tổ chức bộ test

- **Suite** = nhóm case theo chức năng/màn hình hoặc theo kịch bản nghiệp vụ; mã TS-01, TS-02…
- Mã case liên tục trong mô-đun; để khoảng trống giữa các suite (TC-TRI-01…09 cho UI, 10…19 cho ma trận) để chèn sau không phải đánh số lại.
- Trong suite: case positive/happy path trước, rồi negative, rồi biên — trừ khi kịch bản nghiệp vụ đòi thứ tự khác (vd tạo → sửa → xoá).
- Mỗi suite chọn **một** định dạng. Nếu cùng quy trình chỉ khác dữ liệu → ma trận; nếu luồng khác nhau → step-by-step.
- Ma trận truy vết yêu cầu ↔ test case phải cho thấy yêu cầu nào **chưa** được bao phủ.
- Làm nhanh mà không ẩu: dùng template, nhân bản (clone) case tốt rồi thay biến và đọc soát lại, dùng công cụ quản lý test.
