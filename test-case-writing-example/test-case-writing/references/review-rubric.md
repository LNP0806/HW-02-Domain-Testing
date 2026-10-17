# Rubric review & refactor test case

Dùng cho chế độ **Review** (chấm test case có sẵn — người hoặc AI viết) và bước tự kiểm trước khi xuất ở chế độ **Thiết kế/Refactor**.

## Thang điểm 0–2 cho mỗi thuộc tính (tổng /14)

| Thuộc tính | 2 — Đạt | 1 — Một phần | 0 — Không đạt |
|---|---|---|---|
| accurate | Bước và kết quả khớp đúng mục tiêu ở tiêu đề | Có bước lạc đề nhỏ | Tiêu đề và nội dung test hai thứ khác nhau |
| economical | Chỉ các bước cần thiết | 1–2 bước thừa | Lặp lại thiết lập, gộp nhiều mục tiêu |
| repeatable | Dữ liệu cụ thể, kết quả cụ thể | Một chỗ cần tester tự chọn | "nhập giá trị hợp lệ", kết quả mơ hồ |
| traceable | Có mã yêu cầu tồn tại thật | Có nhắc yêu cầu nhưng không mã/mơ hồ | Không truy vết |
| appropriate | Hợp môi trường & đội chạy | Thiếu thông tin môi trường | Sai môi trường/công cụ |
| self_standing | Không phụ thuộc case khác/kiến thức ngầm | Phụ thuộc ngầm nhẹ (thuật ngữ chưa giải thích) | "dùng dữ liệu của test trước" |
| self_cleaning | Có bước dọn dẹp hoặc không tạo dữ liệu | Dọn một phần | Tạo dữ liệu mà không dọn |

**Kết luận (verdict):** `Accept` (≥ 12 và không có lỗi High) · `Revise` (8–11, hoặc có lỗi High sửa được) · `Reject` (< 8, hoặc kết quả mong đợi sai so với spec, hoặc trùng lặp hoàn toàn với case khác).

## Danh mục lỗi (category) — dùng đúng các nhãn này cho nhất quán

| Category | Nhận diện | Mức độ thường gặp |
|---|---|---|
| Wrong expected result | Kết quả mong đợi mâu thuẫn spec (vd 1,1,2 → "Isosceles") | High |
| Fuzzy verdict | "hoạt động đúng", "trông ổn", "hiển thị phù hợp" | High |
| Missing expected result | Bước không có phản hồi hệ thống | High |
| Vague test data | Không có giá trị cụ thể | High |
| Missing step | Thiếu hành động bắt buộc (không nhấn Draw!) | High |
| Broken setup | Tiền điều kiện thiếu/sai | Medium |
| Too long / multi-objective | > 15 bước hoặc nhiều mục tiêu | Medium |
| Stale / invented UI | Tên nút/trường không có trên giao diện hiện tại | Medium |
| Unclear actor | Câu bị động, không rõ ai làm | Low |
| No cleanup | Tạo dữ liệu không xoá | Medium |
| Redundant | Cùng phân hoạch với case khác | Low |
| Not traceable | Không gắn yêu cầu | Low |
| Bad title | Không theo Action + Function + Condition | Low |

Mỗi lỗi ghi: mô tả cụ thể (trích chỗ sai) + cách sửa cụ thể (viết lại câu/giá trị đúng). "Cần rõ hơn" không phải cách sửa.

## Kiểm chứng kết quả mong đợi

Đây là bước quan trọng nhất và là thứ không công cụ lint nào làm được. Với mỗi case: đọc lại yêu cầu trong spec, tự tính kết quả cho dữ liệu đó (với Tam giác: kiểm bất đẳng thức, kiểm vuông bằng Pythagoras, đếm cạnh bằng nhau). Nếu spec không đủ để quyết định → ghi vào Giả định hoặc câu hỏi mở, đừng đoán.

## Khi review một bản review do AI làm (Activity 2)

Lập bảng 3 cột trong `review.ai_review_check`:
- **confirmed** — lỗi AI chỉ ra và bạn xác nhận có thật (kèm bằng chứng: case/bước)
- **false_positives** — AI báo nhưng không phải lỗi (kèm lý do)
- **missed** — lỗi có thật AI bỏ sót

## Refactor test case cũ (Activity 4)

1. Liệt kê từng mục cũ (đoạn văn, dòng) → ghi vào `refactor.mapping[].old` (trích ngắn).
2. Tách mỗi mục tiêu thành một case; mục nhiều mục tiêu → nhiều case mới.
3. Viết lại theo template: mã, tiêu đề A+F+C, mục đích/truy vết, thiết lập, bước + kết quả, dữ liệu cụ thể, dọn dẹp.
4. Kiểm chứng mọi kết quả mong đợi với spec; sửa chỗ bản cũ sai và ghi rõ trong `change`.
5. Những gì bản cũ thiếu mà bạn phải giả định → `meta.assumptions`.
6. Nếu có dùng AI → điền `ai_declaration` (công cụ, prompt chính, đã sửa gì và vì sao, kiểm chứng thế nào).
