#!/usr/bin/env python3
"""Extract text from Unity PDF ebooks into markdown files for skill reference curation."""

import pathlib
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Run: pip install PyMuPDF")
    sys.exit(1)

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "scripts" / "pdf-extracts"


def extract_pdf(pdf_path: pathlib.Path, output_dir: pathlib.Path) -> None:
    """Extract all text from a PDF and write to a markdown file."""
    doc = fitz.open(str(pdf_path))
    stem = pdf_path.stem  # filename without extension

    lines = [f"# {stem}\n", f"\n*Source: {pdf_path.name}*\n\n---\n"]

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text.strip():
            lines.append(f"\n## Page {page_num}\n\n")
            lines.append(text)

    doc.close()

    out_path = output_dir / f"{stem}.md"
    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"  {pdf_path.name} -> {out_path.name} ({len(lines)} chunks)")


def main() -> None:
    pdfs = sorted(REPO_ROOT.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {REPO_ROOT}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Extracting {len(pdfs)} PDFs to {OUTPUT_DIR}/\n")

    for pdf_path in pdfs:
        extract_pdf(pdf_path, OUTPUT_DIR)

    print(f"\nDone. {len(pdfs)} files written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
