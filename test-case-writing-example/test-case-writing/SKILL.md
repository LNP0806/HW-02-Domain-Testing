---
name: test-case-writing
description: Viết, tổ chức và trình bày test case chuẩn (anatomy đầy đủ, tiêu đề Action + Function + Condition, step-by-step hoặc data matrix, 7 thuộc tính chất lượng, checklist review), xuất đồng thời Word (.docx) và Excel (.xlsx) có ma trận truy vết, dropdown trạng thái, đếm tự động. Ba chế độ — thiết kế bộ test case mới từ spec/use case/ảnh màn hình; refactor test case cũ viết lộn xộn sang template chuẩn; review & chấm điểm test case có sẵn (người hoặc AI viết). Dùng khi người dùng nói 'viết test case', 'tài liệu test case', 'test case Word/Excel', 'template test case', 'chuẩn hoá/refactor test case', 'chấm/review test case', 'đánh giá test case AI sinh ra', 'write test cases', 'test case document/spreadsheet', kể cả khi chỉ đưa spec hoặc file test case cũ và bảo 'làm lại cho chuẩn'. Cần phân tích miền tương đương/giá trị biên thì kết hợp domain-testing-design để chọn dữ liệu, nhưng vẫn dùng skill này để trình bày và xuất Word + Excel.
---

# Viết và trình bày test case (Word + Excel)

Skill này dạy *cách tổ chức và trình bày* test case để bất kỳ ai cũng chạy lại được và pass/fail không còn là ý kiến. Nội dung dựa trên bài giảng "Writing Effective Test Cases — AI-First" (Kaner, IEEE 729, Runnels). Đọc `references/test-case-guide.md` trước khi viết — nó chứa anatomy, cú pháp tiêu đề, ba định dạng, 7 thuộc tính, 7 lỗi phổ biến và ví dụ Tam giác làm chuẩn mực mức chi tiết.

Mọi đầu ra đi qua **một file JSON** (`references/json-schema.md`) → `scripts/lint_testcases.py` kiểm tra → `scripts/build_testcase_docs.py` sinh cả `.docx` lẫn `.xlsx`. Làm vậy vì hai định dạng phải khớp nhau từng chữ, và việc dàn trang thủ công tốn công mà dễ sai. Đừng tự viết code python-docx/openpyxl mới trừ khi người dùng muốn bố cục khác hẳn.

## Bước 0 — Xác định chế độ và ngôn ngữ

| Người dùng đưa… | Chế độ |
|---|---|
| spec / use case / ảnh màn hình / mô tả chức năng | **Thiết kế** |
| file test case cũ (văn xuôi, thiếu trường, lộn xộn) + "chuẩn hoá/viết lại" | **Refactor** |
| bộ test case (của sinh viên, của AI, của đội) + "chấm/review/nhận xét" | **Review** |

Ngôn ngữ đầu ra theo ngôn ngữ người dùng (`meta.language`: `vi` hoặc `en`). Giữ nguyên tên trường giao diện như trên màn hình ("Draw!", "Side 1") dù viết tiếng Việt — đó là điều kiện để test case chạy được.

## Bước 1 — Hiểu đối tượng test

1. Rút ra danh sách yêu cầu có mã (dùng mã của spec nếu có, nếu không tự đặt R1, R2… hoặc SRS-x.y). Chúng là xương sống của truy vết.
2. Ghi tên chính xác của mọi trường, nút, thông báo lỗi. Test case nhắc tới nút không tồn tại là lỗi #4 (stale names) — và là lỗi AI hay mắc nhất.
3. Kết quả mong đợi phải suy ra được từ spec. Khi spec thiếu (thông báo lỗi chính xác là gì? giới hạn trên?), hỏi người dùng nếu họ đang có mặt; nếu không, đặt giả định hợp lý và **ghi vào `meta.assumptions`** — giả định ẩn là cách nhanh nhất để có một bộ test sai.

## Bước 2 — Tổ chức bộ test

- Chia **suite** theo chức năng/màn hình hoặc kịch bản nghiệp vụ (TS-01, TS-02…). Thứ tự: theo luồng nghiệp vụ thực tế; trong suite thường là positive → negative → biên.
- Chọn định dạng cho mỗi suite:
  - cùng một quy trình, chỉ dữ liệu thay đổi → **data matrix** (`format: "matrix"`, viết `procedure` một lần, mỗi dòng có `covers` nói rõ lớp/biên nhắm tới);
  - luồng/hành trình UI, ít biến → **step-by-step** (`format: "steps"`).
- Đánh mã `TC-<MÔĐUN>-<NN>`, để khoảng trống giữa các suite (01–09, 10–19…) để chèn sau không phải đánh số lại.

## Bước 3 — Viết từng test case

Mỗi case: **một mục tiêu, dữ liệu cụ thể, kết quả mong đợi kiểm chứng được.**

- **Tiêu đề** = Action + Function + Condition: "Kiểm tra phân loại tam giác khi ba cạnh bằng nhau (4, 4, 4)", "Verify login is rejected with a valid username and wrong password". Tiêu đề thường là phần duy nhất người khác đọc.
- **Mục đích + truy vết**: một câu + mã yêu cầu.
- **Thiết lập**: môi trường, dữ liệu có sẵn, quyền, trạng thái màn hình ban đầu. Không giả định thứ không được tạo ra ở đâu đó.
- **Bước**: câu chủ động, chủ thể rõ ("Nhập…", "Nhấn…"); mỗi bước một phản hồi hệ thống có thể quan sát; ≤ 15 bước.
- **Kết quả mong đợi**: nêu đúng chữ/giá trị/trạng thái quan sát được ("Nhãn 'SCALENE' hiển thị; không tạo phiên đăng nhập"). Các cụm "hoạt động đúng", "hiển thị phù hợp", "như mong đợi", "looks right" là phán quyết mờ — người chạy sẽ không biết pass hay fail.
- **Dọn dẹp**: nếu case tạo/lưu dữ liệu, thêm bước trả môi trường về trạng thái sạch.
- Trước khi sang case kế tiếp, tự hỏi theo 5 tiêu chí Kaner: case này có khả năng bắt lỗi thật không? Có trùng phân hoạch với case khác không? Có phải giá trị "tốt nhất trong loại" không?

**Chế độ Refactor:** làm theo `references/review-rubric.md` mục "Refactor"; điền `refactor.mapping` (cũ → mới → đã sửa gì). Nếu bản cũ có kết quả mong đợi sai, sửa và nói rõ trong `change`.

**Chế độ Review:** đọc `references/review-rubric.md`; chấm mỗi case 0–2 trên 7 thuộc tính, ghi lỗi bằng đúng nhãn category, mỗi lỗi kèm cách sửa cụ thể, rồi verdict. Kiểm chứng *mọi* kết quả mong đợi với spec — đây là chỗ AI hay sai nhất (vd 1,1,2 bị gọi là "Isosceles"). Nếu người dùng muốn, thêm bộ case đã sửa vào `suites` để tài liệu vừa có bảng chấm vừa có bản chuẩn. Khi đối tượng là một bản review do AI làm, điền `review.ai_review_check` (confirmed / false positives / missed).

Nếu người dùng là sinh viên làm bài có dùng AI, hoặc nhắc tới khai báo AI, thêm `ai_declaration`.

## Bước 4 — Lint, build, kiểm tra

```bash
python <skill>/scripts/lint_testcases.py testcases.json        # sửa hết ERROR; xem xét WARN
python <skill>/scripts/build_testcase_docs.py testcases.json --out-dir <outputs> --basename <TênTàiLiệu>
```

Linter bắt lỗi cơ học (tiêu đề thiếu động từ/điều kiện, bước thiếu kết quả, > 15 bước, từ mơ hồ, câu bị động, thiếu dọn dẹp, trùng dữ liệu, yêu cầu chưa bao phủ). Nó **không** biết kết quả mong đợi có đúng không — đó là việc của bạn ở Bước 3. WARN có thể giữ nếu có lý do (ghi vào `notes`).

Sau khi build, mở nhanh để kiểm tra trực quan nếu có LibreOffice (`soffice --headless --convert-to pdf`), rồi giao cả hai file. Lưu kèm file JSON nếu người dùng có thể muốn sửa và build lại.

## Bước 5 — Trả lời người dùng

Ngắn gọn: số test case/suite, yêu cầu nào chưa bao phủ (nếu có), các giả định đã đặt, và (chế độ Review) điểm trung bình + 3 lỗi nổi bật nhất. Không chép lại toàn bộ test case vào chat — chúng đã ở trong file.

## Tài nguyên

- `references/test-case-guide.md` — toàn bộ nguyên tắc + ví dụ (đọc trước khi viết)
- `references/review-rubric.md` — thang chấm 0–2, danh mục lỗi, quy trình refactor/review
- `references/json-schema.md` — cấu trúc JSON và mô tả bố cục đầu ra
- `assets/example-triangle.json` — ví dụ hoàn chỉnh (một suite step-by-step + một suite ma trận)
- `scripts/build_testcase_docs.py`, `scripts/lint_testcases.py`
