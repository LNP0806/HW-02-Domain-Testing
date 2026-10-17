#!/usr/bin/env python3
"""
Lint a test-case JSON file (schema: references/json-schema.md) for the EShop system.
Validates test cases against standard anatomy, EShop requirement conventions,
Action + Function + Condition title syntax, 7 quality attributes, and checks
for vague/fuzzy wording.

Usage: python lint_testcases.py testcases.json
Exit code 1 if any ERROR, 0 otherwise (WARNs are advisory).
"""
import json
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


ACTION_VERBS_EN = {"verify", "validate", "test", "check", "calculate", "print", "run", "confirm", "ensure"}
ACTION_VERBS_VI = ("kiểm tra", "xác minh", "xác nhận", "kiểm chứng", "tính", "in", "chạy", "thử")

VAGUE = [
    # en
    r"\bworks? (properly|correctly|fine|as expected)\b", r"\bcorrectly\b", r"\bproperly\b",
    r"\bas expected\b", r"\blooks? (right|good|ok)\b", r"\bsome (valid|invalid)?\s*\w+",
    r"\bthoroughly\b", r"\betc\.?\b", r"\bappropriate (message|error)\b", r"\bshould work\b",
    # vi
    r"hoạt động (đúng|bình thường|tốt)", r"hiển thị đúng\s*($|[.,;)])", r"\bđúng như mong đợi",
    r"thông báo (lỗi )?phù hợp", r"\bmột (số|vài) giá trị", r"\bv\.v\b",
    r"\bnhập dữ liệu hợp lệ\b", r"\bthông báo lỗi tương ứng\b", r"\bkỹ lưỡng\b",
    r"\btrông ổn\b", r"\bhợp lý\b"
]

PASSIVE_HINTS = [r"\bis entered\b", r"\bare entered\b", r"\bis clicked\b", r"\bđược nhập\b", r"\bđược nhấn\b"]
CREATE_HINTS = [
    r"\bcreate\b", r"\bregister\b", r"\badd\b", r"\bsave\b", r"\bupload\b", r"\binsert\b",
    r"\btạo\b", r"\bđăng ký\b", r"\bthêm\b", r"\blưu\b", r"\btải lên\b", r"\bđặt hàng\b", r"\bcheckout\b"
]
DEPEND_HINTS = [r"previous test", r"test (case )?trước", r"from (my|the) (last|previous)", r"như TC", r"same as TC"]
ID_RE = re.compile(r"^TC-[A-Z0-9]+(-[A-Z0-9]+)*-\d{2,4}$")

msgs = []


def add(level, cid, text):
    msgs.append((level, cid, text))


def has(patterns, text):
    t = (text or "").lower()
    return [p for p in patterns if re.search(p, t)]


def lint(data):
    lang = data.get("meta", {}).get("language", "vi")
    req_ids = {r["id"] for r in data.get("requirements", [])}
    seen = {}
    covered = defaultdict(list)
    data_sigs = defaultdict(list)

    if not data.get("meta", {}).get("title"):
        add("WARN", "meta", "Tài liệu chưa có tiêu đề (meta.title)")
    if not data.get("requirements"):
        add("WARN", "meta", "Chưa định nghĩa danh sách yêu cầu (requirements)")

    for s in data.get("suites", []):
        fmt = s.get("format", "steps")
        sid = s.get("id", "SUITE")
        if fmt == "matrix":
            if not s.get("procedure"):
                add("ERROR", sid, "Suite định dạng ma trận (matrix) thiếu quy trình chung 'procedure'")
            if not s.get("columns"):
                add("ERROR", sid, "Suite định dạng ma trận (matrix) thiếu danh sách cột 'columns'")
            if len(s.get("cases", [])) > 30:
                add("WARN", sid, "Ma trận có hơn 30 dòng — hãy cân nhắc tách suite để thời gian chạy ≤ 20 phút")

        for c in s.get("cases", []):
            cid = c.get("id", "?")
            if cid in seen:
                add("ERROR", cid, f"Mã test case bị trùng lặp: {cid}")
            seen[cid] = True

            if not ID_RE.match(cid):
                add("WARN", cid, f"Mã test case không theo chuẩn TC-<PHÂN_HỆ>-<SỐ> (ví dụ TC-AUTH-001, TC-COUPON-010): {cid}")

            title = (c.get("title") or "").strip()
            if not title:
                add("ERROR", cid, "Thiếu tiêu đề test case")
            else:
                first = title.split()[0].lower()
                tl = title.lower()
                if not (first in ACTION_VERBS_EN or tl.startswith(ACTION_VERBS_VI)):
                    add("WARN", cid, f"Tiêu đề nên bắt đầu bằng động từ hành động (Kiểm tra/Xác minh/Verify/Validate…): '{title[:60]}'")
                cond_words = [" with ", " when ", " if ", " for ", " using ", " khi ", " với ", " nếu ", " trong trường hợp ", " có ", " bằng ", " tại "]
                if not any(w in f" {tl} " for w in cond_words):
                    add("WARN", cid, "Tiêu đề có vẻ thiếu vế ĐIỀU KIỆN (cú pháp Action + Function + Condition)")
                if has(VAGUE, title):
                    add("ERROR", cid, f"Tiêu đề chứa từ ngữ mơ hồ/không kiểm chứng được: {has(VAGUE, title)}")

            reqs = c.get("requirements") or []
            if not reqs:
                add("WARN", cid, "Test case chưa được ánh xạ tới mã yêu cầu nào (requirements)")
            for r in reqs:
                covered[r].append(cid)
                if req_ids and r not in req_ids:
                    add("ERROR", cid, f"Ánh xạ tới mã yêu cầu không tồn tại trong danh mục: '{r}'")

            if fmt == "matrix":
                inputs = c.get("inputs") or {}
                missing = [col for col in s.get("columns", []) if col not in inputs]
                if missing:
                    add("ERROR", cid, f"Dòng ma trận thiếu các cột đầu vào {missing} (hãy ghi '' hoặc '— để trống —')")
                if not c.get("expected_result"):
                    add("ERROR", cid, "Dòng ma trận thiếu kết quả mong đợi (expected_result)")
                elif has(VAGUE, c["expected_result"]):
                    add("ERROR", cid, f"Kết quả mong đợi mơ hồ: {has(VAGUE, c['expected_result'])}")
                sig = tuple(str(inputs.get(k, "")) for k in s.get("columns", []))
                data_sigs[(s.get("id"), sig)].append(cid)
                continue

            # Format step-by-step
            steps = c.get("steps") or []
            if not steps:
                add("ERROR", cid, "Test case step-by-step nhưng không có danh sách các bước (steps)")
            if len(steps) > 15:
                add("ERROR", cid, f"Test case có {len(steps)} bước (> 15 bước) — hãy chia nhỏ mục tiêu kiểm thử")
            if not c.get("preconditions"):
                add("WARN", cid, "Thiếu thiết lập/tiền điều kiện (môi trường, dữ liệu, tài khoản)")

            for i, st in enumerate(steps, 1):
                a, e = st.get("action", ""), st.get("expected", "")
                if not a.strip():
                    add("ERROR", cid, f"Bước {i}: Hành động rỗng (empty action)")
                if not e.strip():
                    add("ERROR", cid, f"Bước {i}: Thiếu phản hồi hệ thống mong đợi (expected system response)")
                v = has(VAGUE, a) + has(VAGUE, e)
                if v:
                    add("ERROR", cid, f"Bước {i}: Chứa từ ngữ mơ hồ: {v}")
                if has(PASSIVE_HINTS, a):
                    add("WARN", cid, f"Bước {i}: Dùng câu bị động — cần chỉ rõ ai là chủ thể hành động (tester hay hệ thống)")
                if has(DEPEND_HINTS, a + " " + " ".join(c.get("preconditions") or [])):
                    add("ERROR", cid, f"Bước {i}: Phụ thuộc vào test case khác — mỗi test case phải độc lập (self-standing)")

            if not c.get("expected_result") and not steps:
                add("ERROR", cid, "Không có kết quả mong đợi tổng quát hoặc theo từng bước")
            if c.get("expected_result") and has(VAGUE, c["expected_result"]):
                add("ERROR", cid, f"Kết quả mong đợi tổng mơ hồ: {has(VAGUE, c['expected_result'])}")

            creates = any(has(CREATE_HINTS, st.get("action", "")) for st in steps)
            if creates and not c.get("cleanup"):
                add("WARN", cid, "Các bước có tạo/ghi dữ liệu nhưng thiếu bước dọn dẹp (cleanup) — vi phạm tính self-cleaning")

            if not c.get("test_data") and not re.search(r"\d|['\"“”‘’]", " ".join(st.get("action", "") for st in steps)):
                add("WARN", cid, "Không thấy dữ liệu kiểm thử cụ thể (giá trị số hoặc chuỗi trong ngoặc kép)")

            sig = (s.get("id"), json.dumps([st.get("action") for st in steps], ensure_ascii=False))
            data_sigs[sig].append(cid)

    for k, ids in data_sigs.items():
        if len(ids) > 1:
            add("WARN", ",".join(ids), "Các test case có dữ liệu/hành động giống hệt nhau — có thể trùng phân hoạch kiểm thử")

    for r in req_ids:
        if r not in covered:
            add("WARN", r, f"Yêu cầu '{r}' chưa được bao phủ bởi test case nào trong bộ test")


def main():
    if len(sys.argv) < 2:
        print("Usage: python lint_testcases.py <testcases.json>")
        return 1

    try:
        data = json.load(open(sys.argv[1], encoding="utf-8"))
    except Exception as ex:
        print(f"[ERROR] Không thể đọc file JSON '{sys.argv[1]}': {ex}")
        return 1

    lint(data)
    n_err = sum(1 for m in msgs if m[0] == "ERROR")
    n_warn = len(msgs) - n_err

    for lvl, cid, text in sorted(msgs, key=lambda m: (m[0] != "ERROR", str(m[1]))):
        print(f"[{lvl}] {cid}: {text}")

    n_cases = sum(len(s.get("cases", [])) for s in data.get("suites", []))
    print(f"\nTổng kết: {n_cases} test cases · {n_err} lỗi (ERROR) · {n_warn} cảnh báo (WARN)")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
