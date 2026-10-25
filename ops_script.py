# count_ops.py  (run from repo root: uv run python count_ops.py)
from odenc.langs import LangVar
from tests.utils import search_test_programs_for
from odenc.langs.lang_var.partial_eval import BinaryOpCounter, PartialEval

lang = LangVar()
counter = BinaryOpCounter()
pe = PartialEval()

total_before = 0
total_after = 0

print(f"{'before':>36}{'after':>36}  program")

for path in sorted(search_test_programs_for(lang), key=str):
    try:
        ast = lang.parse(open(path).read())
    except Exception as e:
        print(f"{'skipped':>36}{type(e).__name__:>36}  {path}")
        continue

    optimized = pe.pe_program(ast)

    before = counter.count(ast)
    after = counter.count(optimized)

    total_before += before
    total_after += after
    print(f"{before:>36}{after:>36}  {path}")

print()
print(f"Total before: {total_before}")
print(f"Total after:  {total_after}")
if total_before > 0:
    removed = total_before - total_after
    print(f"Removed: {removed} ({100 * removed / total_before:.1f}%)")
