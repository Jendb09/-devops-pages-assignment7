"""Minimal release gate for Assignment 7: README + generated HTML checks."""
from pathlib import Path
from html.parser import HTMLParser

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

readme_path = Path("README.md")
index_path = Path("index.md")
site_path = Path("_site/index.html")
for path in (readme_path, index_path, site_path):
    if not path.is_file():
        raise SystemExit(f"FAIL: missing {path}")

readme = readme_path.read_text(encoding="utf-8")
start = "<!--START_SECTION:activity-->"
end = "<!--END_SECTION:activity-->"
if readme.count(start) != 1 or readme.count(end) != 1:
    raise SystemExit("FAIL: README activity markers are missing or duplicated")
if readme.find(start) >= readme.find(end):
    raise SystemExit("FAIL: README activity markers are in the wrong order")

index = index_path.read_text(encoding="utf-8")
if "{% include_relative README.md %}" not in index:
    raise SystemExit("FAIL: homepage does not include README.md")

html = site_path.read_text(encoding="utf-8")
parser = VisibleText()
parser.feed(html)
visible_text = " ".join(parser.parts)
if "Recent activity" not in visible_text:
    raise SystemExit("FAIL: built homepage is missing the activity heading")
if "<!doctype html>" not in html.lower():
    raise SystemExit("FAIL: built homepage is missing an HTML doctype")
print("PASS: activity markers, include, and generated homepage checks")
