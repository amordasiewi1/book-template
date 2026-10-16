# Textbook template

Experimental TeX4ht + make4ht edition, on branch `experiment/make4ht`.
The plasTeX implementation remains on `main`.

Install uv and the system TeX tools. On Ubuntu:

```sh
sudo apt-get install texlive-extra-utils texlive-latex-extra texlive-fonts-recommended
```

Run from the repository root:

```sh
uv sync
uv run book html
uv run book serve
```

Preview at http://localhost:8000; stop with Ctrl+C. Rebuild and refresh after
editing. Use `uv run book pdf` to build the PDF.

The Python wrapper only invokes make4ht, latexmk, or Python's HTTP server.
There are no Python runtime dependencies; uv manages the local command.
TeX4ht and make4ht are system tools, not Python packages.

All LaTeX sources live under `tex/`. Both entry files read `book-content.tex`
and the same parts, chapters, packages, and title metadata. PDF layout stays
in `tex/layout/`. Web conversion settings and Georgia styling are in
`html/book.cfg`. The HTML uses MathJax (internet access required for its CDN)
and splits at parts and chapters.

Outputs:

- PDF: `build/book.pdf`
- Experimental HTML: `build/html-make4ht/index.html`
- HTML build intermediates: `build/make4ht/`

The wrapper copies `tex/` into the HTML build directory before conversion,
so intermediate files stay out of the source tree. This also works with
older make4ht versions that lack the `-B` build-directory flag.

On the Ubuntu TeX Live 2023 installation, make4ht reports that the optional
`char-def` module is missing. Conversion succeeds; automatic section-ID
cleanup is unavailable. Generated links should be checked after upgrades.

Existing plasTeX output in `build/html/` is left alone. Run `uv sync` after
switching branches to synchronize the Python environment.

For simultaneous evaluation, create a second checkout after committing changes:

```sh
git worktree add ../book-template-plastex main
```

That checkout has its own source files, virtual environment, and build output.
No changes are published or pushed automatically.

See the [make4ht documentation](https://www.kodymirus.cz/make4ht/make4ht-doc.html).
