#!/usr/bin/env bash
# convert_to_pdf.sh
# Converts a LaTeX (.tex) file to PDF and places output in resume_pdf/
#
# Usage:
#   ./convert_to_pdf.sh <filename.tex>
#   ./convert_to_pdf.sh              (converts all .tex files in current dir)
#
# Requirements: pdflatex (TeX Live or MacTeX)
#   Install on macOS:  brew install --cask mactex-no-gui
#   Install on Ubuntu: sudo apt-get install texlive-full

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/resume_pdf"
mkdir -p "$OUTPUT_DIR"

# Resolve pdflatex — support both PATH and MacTeX default location
PDFLATEX=""
if command -v pdflatex &>/dev/null; then
  PDFLATEX="pdflatex"
elif [ -x "/Library/TeX/texbin/pdflatex" ]; then
  PDFLATEX="/Library/TeX/texbin/pdflatex"
else
  echo "ERROR: pdflatex not found."
  echo ""
  echo "Install it with one of the following:"
  echo "  macOS:   brew install --cask mactex-no-gui"
  echo "  Ubuntu:  sudo apt-get install texlive-full"
  exit 1
fi

# Determine which .tex files to process
if [ $# -ge 1 ]; then
  TEX_FILES=("$@")
else
  mapfile -t TEX_FILES < <(find "$SCRIPT_DIR" -maxdepth 1 -name "*.tex" | sort)
fi

if [ ${#TEX_FILES[@]} -eq 0 ]; then
  echo "No .tex files found."
  exit 1
fi

TMPDIR_BASE=$(mktemp -d)
trap 'rm -rf "$TMPDIR_BASE"' EXIT

for TEX_FILE in "${TEX_FILES[@]}"; do
  # Resolve absolute path
  if [[ "$TEX_FILE" != /* ]]; then
    TEX_FILE="$SCRIPT_DIR/$TEX_FILE"
  fi

  if [ ! -f "$TEX_FILE" ]; then
    echo "WARNING: File not found: $TEX_FILE — skipping."
    continue
  fi

  BASENAME="$(basename "$TEX_FILE" .tex)"
  OUTPUT_NAME="Manju_Malateshappa_Resume"
  TMPDIR="$TMPDIR_BASE/$BASENAME"
  mkdir -p "$TMPDIR"

  echo "Converting: $BASENAME.tex -> resume_pdf/$OUTPUT_NAME.pdf"

  # Run pdflatex twice for correct page references
  "$PDFLATEX" -interaction=nonstopmode -output-directory="$TMPDIR" "$TEX_FILE" > "$TMPDIR/pdflatex.log" 2>&1
  "$PDFLATEX" -interaction=nonstopmode -output-directory="$TMPDIR" "$TEX_FILE" >> "$TMPDIR/pdflatex.log" 2>&1

  if [ -f "$TMPDIR/$BASENAME.pdf" ]; then
    cp "$TMPDIR/$BASENAME.pdf" "$OUTPUT_DIR/$OUTPUT_NAME.pdf"
    echo "  Done -> $OUTPUT_DIR/$OUTPUT_NAME.pdf"
  else
    echo "  ERROR: PDF generation failed. Check log:"
    tail -20 "$TMPDIR/pdflatex.log"
    exit 1
  fi
done

echo ""
echo "All PDFs saved to: $OUTPUT_DIR"
