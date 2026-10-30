"""Build a notebook from a Python script. Top-of-file docstring -> markdown cell; blocks separated
by lines starting with `# %%` -> code cells; `# %% [markdown]` blocks -> markdown.
Usage: python tools/nb_from_py.py path/to/script.py path/to/out.ipynb
"""
import ast
import sys
from pathlib import Path

import nbformat

src_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
text = src_path.read_text()
module = ast.parse(text)
doc = ast.get_docstring(module)
cells = []
if doc:
    cells.append(nbformat.v4.new_markdown_cell(doc))
    # strip the docstring from the body
    first = module.body[0]
    text = "\n".join(text.splitlines()[first.end_lineno:])
chunks, mode, buf = [], "code", []
for line in text.splitlines():
    if line.startswith("# %%"):
        if "".join(buf).strip():
            chunks.append((mode, "\n".join(buf).strip("\n")))
        buf, mode = [], ("markdown" if "[markdown]" in line else "code")
        title = line.split("# %%", 1)[1].replace("[markdown]", "").strip()
        if title and mode == "code":
            buf.append(f"# {title}")
    else:
        buf.append(line)
if "".join(buf).strip():
    chunks.append((mode, "\n".join(buf).strip("\n")))
for mode, body in chunks:
    if mode == "markdown":
        body = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in body.splitlines())
        cells.append(nbformat.v4.new_markdown_cell(body))
    else:
        cells.append(nbformat.v4.new_code_cell(body))
nb = nbformat.v4.new_notebook(cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3 (.venv)", "language": "python"}})
out_path.parent.mkdir(parents=True, exist_ok=True)
nbformat.write(nb, out_path)
print("wrote", out_path, len(cells), "cells")
