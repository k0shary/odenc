from pathlib import Path
import json

from odenc import Language


def search_test_programs_for(language: Language | str):
    if not isinstance(language, str):
        language = language.name()

    lang_dir = Path(__file__).absolute().parent.parent / "progs" / language
    assert lang_dir.exists()
    prog_file_paths = set(lang_dir.glob("*.odc"))

    inherit = lang_dir / "inherit"
    if inherit.exists():
        with open(inherit, "r") as fin:
            languages = [x.strip() for x in fin if x]

        for lang in languages:
            inherited_files = search_test_programs_for(lang)
            prog_file_paths.update(inherited_files)

    return sorted(prog_file_paths)


def load_test_program(path: Path):
    with open(path, "r") as f:
        lines = f.readlines()

    result = {}
    if len(lines) >= 1 and lines[0].startswith("// TEST"):
        test_line = lines.pop(0).strip()
        test = json.loads(test_line[7:])
        assert isinstance(test, dict)
        assert "code" not in test
        assert "path" not in test
        result = test

    if "in" not in result:
        result["in"] = []
    if "expected_out" not in result:
        result["expected_out"] = []

    result["path"] = path
    result["code"] = "\n".join([line.strip() for line in lines])

    return result
