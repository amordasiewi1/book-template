"""Build shared LaTeX sources as PDF or HTML."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import subprocess
import sys


def project_root() -> Path:
    for candidate in (Path.cwd(), *Path.cwd().parents):
        if (candidate / "book.tex").is_file() and (candidate / "pyproject.toml").is_file():
            return candidate
    raise RuntimeError("Run this command from the textbook repository or a subfolder.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("html", help="Build HTML in build/html")
    commands.add_parser("pdf", help="Build build/book.pdf (requires latexmk)")
    serve = commands.add_parser("serve", help="Preview existing HTML locally")
    serve.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    try:
        root = project_root()
        if args.command == "html":
            executable = Path(sys.executable).parent / "plastex"
            if sys.platform == "win32":
                executable = executable.with_suffix(".exe")
            subprocess.run([
                str(executable), "--renderer=HTML5", "--split-level=0",
                "--dir=build/html", "--extra-css=html/book.css", "html/book.tex",
            ], cwd=root, check=True)
            # plasTeX copies extra CSS by basename but links using its input path.
            css_target = root / "build/html/styles/html/book.css"
            css_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / "html/book.css", css_target)
            print(f"HTML: {root / 'build/html/index.html'}")
        elif args.command == "pdf":
            executable = shutil.which("latexmk")
            if executable is None:
                raise RuntimeError("latexmk is missing. Install a LaTeX distribution first.")
            subprocess.run([
                executable, "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                "-outdir=build", "book.tex",
            ], cwd=root, check=True)
        else:
            directory = root / "build/html"
            if not (directory / "index.html").is_file():
                raise RuntimeError("No HTML build found. Run 'uv run book html' first.")
            handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
            with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
                print(f"Preview: http://localhost:{args.port} (Ctrl+C to stop)", flush=True)
                server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
