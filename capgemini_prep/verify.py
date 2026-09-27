"""Verifies the generated PDF actually contains all 10 sets and every question."""
import re
import sys

from pypdf import PdfReader

PDF = "Capgemini_Exceller_10_Test_Sets.pdf"

reader = PdfReader(PDF)
pages = [p.extract_text() or "" for p in reader.pages]
full = "\n".join(pages)

print("Pages: %d" % len(reader.pages))
print("Extracted characters: %d" % len(full))
print()

SETS = ["Test Set 1", "Test Set 2", "Test Set 3", "Test Set 4", "Test Set 5",
        "Test Set H1", "Test Set H2", "Test Set H3", "Test Set H4",
        "Test Set H5"]

failures = []

# --- 1. every set heading present, and on its own page -------------------
print("--- Set headings (body heading, not the running header) ---")
set_page = {}
for name in SETS:
    # The real heading is immediately followed by the band note line, which
    # distinguishes it from the running header repeated on every page.
    pat = re.compile(re.escape(name) + r"\s*\n\s*(?:Standard|Senior) Analyst band")
    hits = [i for i, t in enumerate(pages) if pat.search(t)]
    if len(hits) == 1:
        set_page[name] = hits[0]
        print("  OK   %-14s starts on page %d" % (name, hits[0] + 1))
    elif not hits:
        failures.append("missing set heading: %s" % name)
        print("  FAIL %-14s heading NOT FOUND" % name)
    else:
        failures.append("duplicate heading for %s on pages %s" % (name, hits))
        print("  FAIL %-14s heading found %d times" % (name, len(hits)))

# --- 2. per-set question numbering ---------------------------------------
# Slice the document by set start page, then count Q markers in that slice.
print()
print("--- Question counts per set ---")
order = sorted(set_page.items(), key=lambda kv: kv[1])

# Part-banner pages are boundaries too; they belong to no set.
PART_BANNERS = ["How To Use This Book", "Notation Reference",
                "Part Two - Senior Analyst Band", "Answer Keys",
                "Traps Worth Reviewing", "Sources And Attribution"]
part_pages = sorted({i for i, t in enumerate(pages)
                     for b in PART_BANNERS if b in t})
keys_page = next((i for i, t in enumerate(pages) if "Answer Keys" in t),
                 len(pages))

boundaries = sorted(set(p for _, p in order) | set(part_pages) | {len(pages)})
bounds = []
for name, start in order:
    end = next(b for b in boundaries if b > start)
    bounds.append((name, start, end))
print("  (part-banner pages: %s)" % [p + 1 for p in part_pages])
print("  (Answer Keys part begins on page %d)" % (keys_page + 1))

for name, start, end in bounds:
    chunk = "\n".join(pages[start:end])
    nums = set()
    for m in re.finditer(r"Q(\d{1,2})\.", chunk):
        nums.add(int(m.group(1)))
    expected_max = 44
    missing = [n for n in range(1, expected_max + 1) if n not in nums]
    # Sets 1-5 use Q41-44 for games; H sets use Q39-44. Both end at 44.
    status = "OK  " if not missing else "FAIL"
    if missing:
        failures.append("%s missing question numbers %s" % (name, missing))
    print("  %s %-14s found %d of %d question numbers%s"
          % (status, name, len(nums), expected_max,
             "" if not missing else "  missing=%s" % missing))

# --- 3. structural sections present in every set ------------------------
print()
print("--- Section headings per set ---")
need = ["Section A - Pseudo-code", "Section A - Computer Fundamentals",
        "Section B - English Communication", "Section C - Game-Based Cognitive",
        "Section D - Coding Round"]
for name, start, end in bounds:
    chunk = "\n".join(pages[start:end])
    missing = [s for s in need if s not in chunk]
    status = "OK  " if not missing else "FAIL"
    if missing:
        failures.append("%s missing sections %s" % (name, missing))
    print("  %s %-14s %s" % (status, name,
                             "all 5 sections" if not missing
                             else "missing %s" % missing))

# --- 3b. running header must name the set that owns each page ------------
print()
print("--- Running header correctness ---")
for name, start, end in bounds:
    last = (end if end is not None else len(pages)) - 1
    bad = []
    for p in range(start, last + 1):
        first_line = (pages[p].lstrip().split("\n") or [""])[0].strip()
        if first_line != name:
            bad.append((p + 1, first_line))
    status = "OK  " if not bad else "FAIL"
    if bad:
        failures.append("%s wrong header on pages %s"
                        % (name, [b[0] for b in bad]))
    print("  %s %-14s pages %d-%d%s"
          % (status, name, start + 1, last + 1,
             "" if not bad else "  wrong on %s" % bad[:3]))

# --- 3c. non-set pages must NOT carry a set running header ---------------
print()
print("--- Non-set pages carry no set header ---")
leaked = []
for p in range(keys_page, len(pages)):
    first_line = (pages[p].lstrip().split("\n") or [""])[0].strip()
    if first_line in SETS:
        leaked.append(p + 1)
if leaked:
    failures.append("set header leaked onto non-set pages %s" % leaked)
    print("  FAIL header leaked onto pages %s" % leaked)
else:
    print("  OK   pages %d-%d carry no set header"
          % (keys_page + 1, len(pages)))

# --- 4. front matter, part banners, answer keys -------------------------
print()
print("--- Structural parts ---")
markers = [
    "How To Use This Book",
    "Notation Reference",
    "switchChallenge - how the operator works",
    "Part Two - Senior Analyst Band",
    "Answer Keys",
    "Traps Worth Reviewing",
    "Sources And Attribution",
]
for m in markers:
    ok = m in full
    if not ok:
        failures.append("missing part: %s" % m)
    print("  %s %s" % ("OK  " if ok else "FAIL", m))

# --- 5. answer key block for each of the 10 sets ------------------------
print()
print("--- Answer key blocks ---")
key_start = full.find("Answer Keys")
key_text = full[key_start:] if key_start >= 0 else ""
for name in SETS:
    label = name.replace("Test Set ", "Set ")
    # key section headings are "Set 1", "Set H1", ...
    ok = re.search(r"%s\s" % re.escape(label), key_text) is not None
    if not ok:
        failures.append("missing answer key for %s" % name)
    print("  %s answer key for %s" % ("OK  " if ok else "FAIL", label))

# --- 6. spot-check that code blocks survived -----------------------------
print()
print("--- Pseudo-code rendering spot checks ---")
spot = [
    "Set a = 8, b = 3",
    "for(each i from 1 to 6)",
    "End function solve()",
    "Integer M[3][3], i, s",
    "while(i < j AND A[i] MOD 2 == 1)",
    "Operator 1    3142",
    "MISSISSIPPI",
]
for s in spot:
    ok = s in full
    if not ok:
        failures.append("code text not rendered: %s" % s)
    print("  %s %s" % ("OK  " if ok else "FAIL", s))

print()
if failures:
    print("VERIFICATION FAILED - %d problem(s):" % len(failures))
    for f in failures:
        print("   - %s" % f)
    sys.exit(1)
print("VERIFICATION PASSED - all 10 sets complete and rendered.")
