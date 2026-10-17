#!/usr/bin/env python3
"""
Lint a test-case JSON file (schema: references/json-schema.md) against the
presentation/organisation rules of the skill. Mechanical checks only — they
catch the easy-to-miss problems; a human/LLM review is still needed for
correctness of expected results.

Usage: python lint_testcases.py testcases.json
Exit code 1 if any ERROR, 0 otherwise (WARNs are advisory).
"""
import json
import re
import sys
from collections import defaultdict

ACTION_VERBS_EN = {"verify", "validate", "test", "check", "calculate", "print", "run", "confirm", "ensure"}
ACTION_VERBS_VI = ("kiểm tra", "xác minh", "xác nhận", "kiểm chứng", "tính", "in", "chạy", "thử")
VAGUE = [
    # en
    r"\bworks? (properly|correctly|fine|as expected)\b", r"\bcorrectly\b", r"\bproperly\b",
    r"\bas expected\b", r"\blooks? (right|good|ok)\b", r"\bsome (valid|invalid)?\s*\w+",
    r"\bthoroughly\b", r"\betc\.?\b", r"\bappropriate (message|error)\b", r"\bshould work\b",
    # vi
    r"hoạt động (đúng|bình thường|tốt)", r"hiển thị đúng\s*($|[.,;)])", r"\bđúng như mong đợi", r"thông báo (lỗi )?phù hợp",
    r"\bmột (số|vài) giá trị", r"\bv\.v\b", r"\bnhập dữ liệu hợp lệ\b", r"\bthông báo lỗi tương ứng\b",
    r"\bkỹ lưỡng\b",
]
PASSIVE_HINTS = [r"\bis entered\b", r"\bare entered\b", r"\bis clicked\b", r"\bđược nhập\b", r"\bđược nhấn\b"]
CREATE_HINTS = [r"\bcreate\b", r"\bregister\b", r"\badd\b", r"\bsave\b", r"\bupload\b", r"\binsert\b",
                r"\btạo\b", r"\bđăng ký\b", r"\bthêm\b", r"\blưu\b", r"\btải lên\b"]
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

    for s in data.get("suites", []):
        fmt = s.get("format", "steps")
        if fmt == "matrix":
            if not s.get("procedure"):
                add("ERROR", s.get("id"), "matrix suite has no common 'procedure' — the reader cannot run the rows")
            if not s.get("columns"):
                add("ERROR", s.get("id"), "matrix suite has no 'columns'")
            if len(s.get("cases", [])) > 25:
                add("WARN", s.get("id"), "matrix > 25 rows — check it still runs in ≤ 20 minutes or split it")
        for c in s.get("cases", []):
            cid = c.get("id", "?")
            if cid in seen:
                add("ERROR", cid, "duplicate test case ID")
            seen[cid] = True
            if not ID_RE.match(cid):
                add("WARN", cid, "ID does not follow TC-<MODULE>-<NN> convention")
            title = (c.get("title") or "").strip()
            if not title:
                add("ERROR", cid, "missing title")
            else:
                first = title.split()[0].lower()
                tl = title.lower()
                if not (first in ACTION_VERBS_EN or tl.startswith(ACTION_VERBS_VI)):
                    add("WARN", cid, f"title should start with an action verb (Verify/Validate/Test… | Kiểm tra/Xác minh…): '{title[:60]}'")
                cond_words = [" with ", " when ", " if ", " for ", " using ", " khi ", " với ", " nếu ", " trong trường hợp ", " có ", " bằng "]
                if not any(w in f" {tl} " for w in cond_words):
                    add("WARN", cid, "title seems to lack a CONDITION part (Action + Function + Condition)")
                if has(VAGUE, title):
                    add("ERROR", cid, f"vague wording in title: {has(VAGUE, title)}")
            reqs = c.get("requirements") or []
            if not reqs:
                add("WARN", cid, "not traced to any requirement")
            for r in reqs:
                covered[r].append(cid)
                if req_ids and r not in req_ids:
                    add("ERROR", cid, f"traces to unknown requirement '{r}'")

            if fmt == "matrix":
                inputs = c.get("inputs") or {}
                missing = [col for col in s.get("columns", []) if col not in inputs]
                if missing:
                    add("ERROR", cid, f"matrix row missing input columns {missing} (use '' or '— blank —' explicitly)")
                if not c.get("expected_result"):
                    add("ERROR", cid, "matrix row has no expected_result")
                elif has(VAGUE, c["expected_result"]):
                    add("ERROR", cid, f"fuzzy expected result: {has(VAGUE, c['expected_result'])}")
                sig = tuple(str(inputs.get(k, "")) for k in s.get("columns", []))
                data_sigs[(s.get("id"), sig)].append(cid)
                continue

            steps = c.get("steps") or []
            if not steps:
                add("ERROR", cid, "step-by-step case has no steps")
            if len(steps) > 15:
                add("ERROR", cid, f"{len(steps)} steps (> 15) — split into smaller objectives")
            if not c.get("preconditions"):
                add("WARN", cid, "no setup/preconditions — environment, data, access?")
            for i, st in enumerate(steps, 1):
                a, e = st.get("action", ""), st.get("expected", "")
                if not a.strip():
                    add("ERROR", cid, f"step {i}: empty action")
                if not e.strip():
                    add("ERROR", cid, f"step {i}: no expected system response")
                v = has(VAGUE, a) + has(VAGUE, e)
                if v:
                    add("ERROR", cid, f"step {i}: vague wording {v}")
                if has(PASSIVE_HINTS, a):
                    add("WARN", cid, f"step {i}: passive voice — who acts, tester or system?")
                if has(DEPEND_HINTS, a + " " + " ".join(c.get("preconditions") or [])):
                    add("ERROR", cid, f"step {i}: depends on another test — must be self-standing")
            if not c.get("expected_result") and not steps:
                add("ERROR", cid, "no expected result anywhere")
            if c.get("expected_result") and has(VAGUE, c["expected_result"]):
                add("ERROR", cid, f"fuzzy overall expected result: {has(VAGUE, c['expected_result'])}")
            creates = any(has(CREATE_HINTS, st.get("action", "")) for st in steps)
            if creates and not c.get("cleanup"):
                add("WARN", cid, "steps create/save data but no cleanup — is it self-cleaning?")
            if not c.get("test_data") and not re.search(r"\d|['\"“”‘’]", " ".join(st.get("action", "") for st in steps)):
                add("WARN", cid, "no concrete test data visible (numbers/quoted values)")
            sig = (s.get("id"), json.dumps([st.get("action") for st in steps], ensure_ascii=False))
            data_sigs[sig].append(cid)

    for k, ids in data_sigs.items():
        if len(ids) > 1:
            add("WARN", ",".join(ids), "identical data/steps — redundant cases?")
    for r in req_ids:
        if r not in covered:
            add("WARN", r, "requirement not covered by any test case")


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    lint(data)
    n_err = sum(1 for m in msgs if m[0] == "ERROR")
    n_warn = len(msgs) - n_err
    for lvl, cid, text in sorted(msgs, key=lambda m: (m[0] != "ERROR", str(m[1]))):
        print(f"[{lvl}] {cid}: {text}")
    n_cases = sum(len(s.get("cases", [])) for s in data.get("suites", []))
    print(f"\n{n_cases} test cases · {n_err} errors · {n_warn} warnings")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
