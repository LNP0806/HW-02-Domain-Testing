# JSON đầu vào cho `build_testcase_docs.py` và `lint_testcases.py`

Một file JSON duy nhất sinh ra **cả** Word và Excel, nên hai bản luôn khớp nhau. Ví dụ đầy đủ: `assets/example-triangle.json`.

```jsonc
{
  "meta": {
    "language": "vi",            // "vi" | "en" — ngôn ngữ nhãn trong file xuất; theo ngôn ngữ người dùng
    "title": "Tài liệu test case — <Hệ thống>",
    "project": "...", "feature": "...",
    "doc_id": "TCD-<MÔĐUN>-01", "version": "1.0", "date": "YYYY-MM-DD",
    "author": "...", "reviewer": "",
    "sut_version": "phiên bản phần mềm được test",
    "environment": "trình duyệt/OS/thiết bị",
    "scope": "đoạn văn phạm vi",
    "references": ["..."],
    "assumptions": ["mọi giả định bạn tự đặt khi spec thiếu"]
  },
  "requirements": [ {"id": "SRS-3.1", "text": "..."} ],   // dùng cho ma trận truy vết
  "suites": [
    {
      "id": "TS-01", "name": "...", "description": "...",
      "format": "steps",                // step-by-step
      "cases": [
        {
          "id": "TC-<MÔĐUN>-01",
          "title": "Action + Function + Condition",
          "purpose": "mục tiêu một câu",
          "requirements": ["SRS-3.1"],
          "priority": "High|Medium|Low",
          "type": "Positive|Negative|Boundary|...",
          "method": "Manual|Automated",
          "origin": "Human|AI|Both",     // tuỳ chọn (Activity 3)
          "preconditions": ["..."],
          "test_data": "giá trị cụ thể",  // chuỗi hoặc mảng
          "steps": [ {"action": "...", "expected": "..."} ],
          "expected_result": "tiêu chí pass tổng",
          "cleanup": ["..."],
          "status": "Not run", "actual_result": "", "bug_id": "", "notes": ""
        }
      ]
    },
    {
      "id": "TS-02", "name": "...", "format": "matrix",   // ma trận dữ liệu
      "preconditions": ["..."],
      "procedure": [ {"action": "...", "expected": "..."} ],  // viết MỘT lần
      "columns": ["Side 1", "Side 2", "Side 3"],
      "cleanup": ["..."],
      "cases": [
        {"id": "TC-TRI-10", "title": "...", "inputs": {"Side 1": "3", "Side 2": "4", "Side 3": "5"},
         "expected_result": "RIGHT", "covers": "lớp/biên nhắm tới", "requirements": ["SRS-3.1"],
         "priority": "High", "status": "Not run"}
      ]
    }
  ],

  // ---- tuỳ chọn: chế độ Review ----
  "review": {
    "source": "file/đối tượng được review",
    "summary": "nhận xét chung",
    "items": [
      {"case_id": "TC-OLD-01",
       "scores": {"accurate": 2, "economical": 1, "repeatable": 0, "traceable": 1,
                  "appropriate": 2, "self_standing": 2, "self_cleaning": 2},
       "verdict": "Accept|Revise|Reject",
       "defects": [ {"category": "Fuzzy verdict", "severity": "High",
                     "description": "...", "fix": "..."} ] }
    ],
    "checklist": [ {"item": "...", "result": "Có|Không|Một phần", "note": "..."} ],  // bỏ trống → dùng checklist mặc định
    "ai_review_check": {"confirmed": ["..."], "false_positives": ["..."], "missed": ["..."]}  // khi kiểm chứng review của AI
  },

  // ---- tuỳ chọn: chế độ Refactor ----
  "refactor": {
    "source": "file cũ",
    "mapping": [ {"old": "trích mục cũ", "new": ["TC-TRI-01", "TC-TRI-02"], "change": "đã sửa gì"} ]
  },

  // ---- tuỳ chọn: khai báo dùng AI ----
  "ai_declaration": {"tool": "...", "prompts": ["..."], "changes": ["..."], "verification": "..."}
}
```

## Đầu ra

**Word** (dọc, A4): thông tin tài liệu → 1 Giới thiệu (phạm vi, tham chiếu, giả định, quy ước) → 2 Yêu cầu & ma trận truy vết (đánh dấu ⚠ yêu cầu chưa bao phủ) → 3 Bảng tổng hợp test case → 4 Chi tiết (mỗi case step-by-step là một khối template; mỗi ma trận là quy trình chung + bảng dữ liệu) → [Review] → [Refactor map] → [Khai báo AI].

**Excel**: `Tổng quan` (thông tin + đếm trạng thái bằng COUNTIF, tự cập nhật khi tester đổi trạng thái) · `Test Cases` (một dòng/bước, cột cấp case được gộp ô; dropdown trạng thái tô màu Pass/Fail/Blocked; lọc, cố định tiêu đề) · một sheet cho mỗi suite ma trận · `Truy vết` (ma trận yêu cầu × test case, #TC tô đỏ khi = 0) · `Review` (khi có) · `Checklist`.

Nếu chỉ cần một định dạng: `--docx-only` hoặc `--xlsx-only`.
