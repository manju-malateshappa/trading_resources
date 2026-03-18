# Resume PDF Generation

PDFs are generated from the `.tex` source files in `docs/resumes/` using the `convert_to_pdf.sh` script.

## Prerequisites

Install `pdflatex` via MacTeX (macOS) or TeX Live (Linux):

```bash
# macOS
brew install --cask mactex-no-gui

# Ubuntu / Debian
sudo apt-get install texlive-full
```

After installing on macOS, reload your PATH:

```bash
eval "$(/usr/libexec/path_helper)"
```

## Usage

From the `docs/resumes/` directory:

```bash
# Convert a specific file
./convert_to_pdf.sh manju_malateshappa_resume_v1.tex

# Convert all .tex files at once
./convert_to_pdf.sh
```

Output PDFs are saved to this `resume_pdf/` directory.

## Resume files

| File | Description |
|------|-------------|
| `manju_malateshappa_resume_v1.tex` | Current version — 2-page, correct header layout |
| `manju_malateshappa_resume_backup.tex` | Backup of first generated version |
| `manju_malateshappa_resume.tex` | Initial attempt |
