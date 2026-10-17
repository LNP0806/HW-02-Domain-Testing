# Cấu Trúc File JSON Kiểm Thử EShop (JSON Schema)

File JSON này là nguồn chân lý duy nhất (Single Source of Truth) để cấp dữ liệu cho `lint_testcases.py` kiểm tra tĩnh và `build_testcase_docs.py` tự động xuất bản đồng thời tài liệu **Word (.docx)** và bảng tính **Excel (.xlsx)**.

---

## 1. Cấu Trúc Tổng Thể

```jsonc
{
  "meta": {
    "language": "vi",                  // "vi" | "en" — Ngôn ngữ nhãn xuất tài liệu
    "title": "Tài liệu Test Case — Hệ thống EShop",
    "project": "EShop SUT",
    "feature": "Pool B: Mã Giảm Giá & Thanh Toán (FR-08, FR-09)",
    "doc_id": "TCD-ESHOP-02",
    "version": "1.0",
    "date": "2026-10-17",
    "author": "Sinh viên Kiểm thử Phần mềm (23120321)",
    "reviewer": "Giảng viên bộ môn / QA Lead",
    "sut_version": "EShop v2.0 (React Web, Express API, SQLite, Expo Mobile)",
    "environment": "Chrome 129 trên Windows 11; Expo Go trên Android 14; Node.js v20",
    "scope": "Kiểm thử miền và giá trị biên cho chức năng áp dụng mã giảm giá và thanh toán trực tuyến.",
    "references": [
      "Đặc tả hệ thống EShop (System Requirements Specification v2.0)",
      "Tài liệu đặc tả API Backend (api_specification.md)",
      "ISTQB Foundation Level Syllabus"
    ],
    "assumptions": [
      "CSDL ban đầu đã được seed đầy đủ danh mục và các mã giảm giá mẫu (SAVE10, BIGBUY, VIP100, EXPIRED).",
      "Tài khoản kiểm thử test@eshop.com đã được tạo sẵn trong SQLite."
    ]
  },

  // Danh sách yêu cầu phục vụ ma trận truy vết (Traceability Matrix)
  "requirements": [
    {"id": "FR-08", "text": "Thanh toán đơn hàng cho người dùng đã đăng nhập; server tự tính lại tổng tiền."},
    {"id": "FR-09", "text": "Áp dụng mã giảm giá tại bước Checkout khi thỏa mãn 5 điều kiện C1-C5."}
  ],

  // Các bộ test suite (chứa các test case)
  "suites": [
    {
      "id": "TS-01",
      "name": "Luồng Giao Diện Áp Dụng Mã & Thanh Toán",
      "format": "steps",              // "steps" = từng bước (step-by-step)
      "description": "Các kịch bản kiểm thử hành trình UI từ giỏ hàng, áp dụng coupon và đặt hàng thành công.",
      "cases": [
        {
          "id": "TC-COUPON-001",
          "title": "Kiểm tra áp dụng mã SAVE10 thành công khi giỏ hàng đạt 300.000 ₫",
          "purpose": "Xác nhận yêu cầu FR-09: người dùng đăng nhập được giảm 10% khi đơn đạt đúng ngưỡng tối thiểu.",
          "requirements": ["FR-09", "FR-08"],
          "priority": "High",
          "type": "Positive",
          "method": "Manual",
          "origin": "Human",          // "Human" | "AI" | "Both"
          "preconditions": [
            "Tài khoản test@eshop.com đã đăng nhập thành công",
            "Giỏ hàng có 1 sản phẩm có giá trị đúng 300.000 ₫",
            "Mã SAVE10 đang active và user chưa từng sử dụng"
          ],
          "test_data": "code: SAVE10, min_order_amount: 300000, discount_value: 10%",
          "steps": [
            {
              "action": "Truy cập vào trang Giỏ hàng và bấm nút 'Thanh toán'",
              "expected": "Chuyển hướng đến trang Checkout; hiển thị danh sách sản phẩm và tổng tiền là 300.000 ₫"
            },
            {
              "action": "Nhập 'SAVE10' vào ô 'Mã giảm giá' và bấm nút 'Áp dụng'",
              "expected": "Hiển thị thông báo áp dụng thành công; xuất hiện dòng chiết khấu -30.000 ₫; tổng thanh toán cập nhật còn 270.000 ₫"
            },
            {
              "action": "Bấm nút 'Thanh toán' (Submit Order)",
              "expected": "Hiển thị thông báo đặt hàng thành công; chuyển hướng sang Lịch sử đơn hàng; giỏ hàng bị xóa sạch"
            }
          ],
          "expected_result": "Đơn hàng được tạo thành công với số tiền 270.000 ₫; ghi nhận 1 lượt sử dụng mã SAVE10 trong bảng coupon_usage.",
          "cleanup": [
            "Khôi phục giỏ hàng hoặc xóa bản ghi đơn hàng vừa tạo trong SQLite để giữ sạch môi trường"
          ],
          "status": "Not run",        // "Not run" | "Pass" | "Fail" | "Blocked" | "Skipped"
          "actual_result": "",
          "bug_id": "",
          "notes": ""
        }
      ]
    },

    {
      "id": "TS-02",
      "name": "Ma Trận Kiểm Thử Miền & Giá Trị Biên Cho Coupon",
      "format": "matrix",             // "matrix" = ma trận dữ liệu (data matrix)
      "description": "Kiểm thử các giá trị biên ngưỡng đơn hàng, hạn dùng và số lần dùng của mã giảm giá.",
      "preconditions": [
        "Người dùng đã đăng nhập tài khoản test@eshop.com",
        "Đang ở màn hình Checkout"
      ],
      "procedure": [
        {"action": "Nhập giá trị tại cột 'Coupon Code' vào ô mã giảm giá", "expected": "Ô hiển thị đúng chuỗi ký tự đã nhập"},
        {"action": "Cập nhật giỏ hàng có tổng tiền tại cột 'Tổng Tiền Đơn'", "expected": "Tổng đơn hàng hiển thị tương ứng"},
        {"action": "Bấm nút 'Áp dụng'", "expected": "Hệ thống phản hồi theo đúng cột 'Kết Quả Mong Đợi'"}
      ],
      "columns": ["Coupon Code", "Tổng Tiền Đơn", "Trạng Thái Mã", "Lượt Đã Dùng"],
      "cleanup": ["Làm mới trang Checkout và đặt lại giỏ hàng"],
      "cases": [
        {
          "id": "TC-COUPON-010",
          "title": "Kiểm tra mã SAVE10 với tổng đơn hàng 299.999 ₫ (ngay dưới ngưỡng biên)",
          "inputs": {
            "Coupon Code": "SAVE10",
            "Tổng Tiền Đơn": "299.999 ₫",
            "Trạng Thái Mã": "Active",
            "Lượt Đã Dùng": "0"
          },
          "expected_result": "Báo lỗi: 'Đơn hàng chưa đạt giá trị tối thiểu 300.000 ₫'; không giảm giá",
          "covers": "Biên dưới (Boundary - 1) của điều kiện C3",
          "requirements": ["FR-09"],
          "priority": "High",
          "status": "Not run"
        },
        {
          "id": "TC-COUPON-011",
          "title": "Kiểm tra mã SAVE10 với tổng đơn hàng 300.000 ₫ (chính xác trên biên)",
          "inputs": {
            "Coupon Code": "SAVE10",
            "Tổng Tiền Đơn": "300.000 ₫",
            "Trạng Thái Mã": "Active",
            "Lượt Đã Dùng": "0"
          },
          "expected_result": "Áp dụng thành công; giảm 30.000 ₫; tổng thanh toán là 270.000 ₫",
          "covers": "Biên chính xác (Boundary) của điều kiện C3",
          "requirements": ["FR-09"],
          "priority": "High",
          "status": "Not run"
        }
      ]
    }
  ],

  // ---- Tuỳ chọn: Chế độ Review (Đánh giá chất lượng test case) ----
  "review": {
    "source": "Bộ test case do AI sinh ra ban đầu cho tính năng Giỏ Hàng",
    "summary": "AI bao phủ tốt luồng cơ bản nhưng bỏ sót kiểm thử biên tổng tiền và bịa đặt nhãn nút bấm.",
    "items": [
      {
        "case_id": "TC-OLD-01",
        "scores": {
          "accurate": 2, "economical": 1, "repeatable": 0, "traceable": 1,
          "appropriate": 2, "self_standing": 2, "self_cleaning": 0
        },
        "verdict": "Revise",
        "defects": [
          {
            "category": "Vague test data",
            "severity": "High",
            "description": "Bước 2 ghi 'nhập vài sản phẩm giá hợp lệ' mà không có giá trị số cụ thể.",
            "fix": "Ghi rõ: Chọn 1 iPhone 15 Pro Max số lượng 1, giá 30.000.000 ₫."
          },
          {
            "category": "No cleanup",
            "severity": "Medium",
            "description": "Không có bước hoàn trả giỏ hàng sau khi test.",
            "fix": "Bổ sung bước dọn dẹp: Bấm nút Xóa sản phẩm khỏi giỏ hàng."
          }
        ]
      }
    ],
    "ai_review_check": {
      "confirmed": [
        "TC-OLD-01 thiếu dữ liệu kiểm thử cụ thể và không có bước dọn dẹp"
      ],
      "false_positives": [
        "AI báo rằng mã SAVE10 phải giảm 20% là sai — spec quy định rõ SAVE10 giảm 10%"
      ],
      "missed": [
        "AI không phát hiện ra nút Checkout trong code Frontend thực tế cho phép sửa ô input tổng tiền"
      ]
    }
  },

  // ---- Tuỳ chọn: Chế độ Refactor (Chuẩn hóa test case cũ) ----
  "refactor": {
    "source": "File Excel nháp cũ của nhóm test",
    "mapping": [
      {
        "old": "Dòng 4: Kiểm tra nhập mã giảm giá",
        "new": ["TC-COUPON-001", "TC-COUPON-010", "TC-COUPON-011"],
        "change": "Tách 1 dòng văn xuôi thành 1 test case luồng UI và 2 test case kiểm thử biên 299.999 ₫ và 300.000 ₫."
      }
    ]
  },

  // ---- Tuỳ chọn: Khai báo AI Audit Report ----
  "ai_declaration": {
    "tool": "Gemini 3.8 Flash (via Antigravity Pairing Assistant)",
    "prompts": [
      "Bóc tách biến miền và phân hoạch tương đương cho tính năng FR-09 Coupon",
      "Sinh bảng quyết định 5 điều kiện C1..C5 cho mã giảm giá EShop"
    ],
    "changes": [
      "Sửa lại các nhãn nút bấm theo đúng file frontend-web/src/pages/Checkout.jsx",
      "Bổ sung bước dọn dẹp CSDL cho tất cả các case có thao tác tạo đơn hàng"
    ],
    "verification": "Đã chạy đối chiếu trực tiếp trên hệ thống EShop đang chạy ở http://localhost:5173 và backend http://localhost:3000."
  }
}
```
