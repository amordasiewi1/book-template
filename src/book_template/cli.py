"""Small wrappers around the book's command-line build tools."""

import argparse
from pathlib import Path
import subprocess
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "build/html-make4ht"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["html", "pdf", "serve"])
    command = parser.parse_args().command
    working = ROOT / "tex"
    if command == "html":
        working = ROOT / "build/make4ht"
        shutil.copytree(ROOT / "tex", working, dirs_exist_ok=True)
        args = ["make4ht", "-c", str(ROOT / "html/book.cfg"), "-j", "index",
                "-d", str(HTML),
                "book-html.tex", "mathjax,2"]
    elif command == "pdf":
        args = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                f"-outdir={ROOT / 'build'}", "book.tex"]
    else:
        print("Preview: http://localhost:8000 (Ctrl+C to stop)", flush=True)
        args = [sys.executable, "-m", "http.server", "8000", "--bind", "127.0.0.1",
                "--directory", str(HTML)]
    try:
        return subprocess.run(args, cwd=working).returncode
    except FileNotFoundError:
        parser.exit(1, f"Missing command: {args[0]}. See README.md for installation.\n")
    except KeyboardInterrupt:
        return 0
