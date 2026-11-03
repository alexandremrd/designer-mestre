import pathlib
import py_compile
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {".git", "node_modules"}


def test_skill_has_frontmatter():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---")
    assert re.search(r'^name:\s*"?designer-mestre"?\s*$', text.split("---")[1], re.M)


def test_python_scripts_compile():
    for p in ROOT.rglob("*.py"):
        if SKIP & set(p.parts):
            continue
        py_compile.compile(str(p), doraise=True)
