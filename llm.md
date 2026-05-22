# Aspose MCP Servers — LLM Reference

Compact reference for language models reasoning about Aspose MCP server capabilities.

---

## What these servers are

A collection of MCP servers that expose [Aspose](https://www.aspose.com/) document
processing APIs as callable tools. Each Aspose product (Words, PDF, Cells, etc.) runs
as a separate MCP server process with its own isolated Python environment.

---

## Architecture constraints

- **One server per product.** There is no unified server. Each file format family has
  its own server entry in the MCP host config.
- **File-based I/O.** All tools read from and write to a single shared directory
  (`ASPOSE_FILES_PATH`). Tools do not stream data or accept raw bytes.
- **Bare filenames only.** Tool parameters that accept file paths always expect a bare
  filename (`"report.docx"`), never a full or relative path. The server resolves the
  full path internally.
- **No cross-product tool calls.** A Words tool cannot process a PDF. Route by source
  format, not target format.

---

## Server inventory

### Document formats

| Server | Pypi package | Primary formats | Typical tools |
|--------|-------------|-----------------|---------------|
| `aspose-words` | aspose-words | DOCX, DOC, RTF, ODT, MD | convert, merge, split, extract text, mail merge, protect |
| `aspose-pdf` | aspose-pdf | PDF | convert, merge, split, extract, sign, watermark, compress |
| `aspose-cells` | aspose-cells-python | XLSX, XLS, CSV, ODS | read, write, convert, chart, formula evaluation |
| `aspose-slides` | aspose-slides | PPTX, PPT, ODP | convert, merge, extract, add/remove slides, export images |
| `aspose-email` | aspose-email-for-python-via-net | MSG, EML, PST, MBOX, MHTML | read, convert, extract attachments, parse headers |

### Image and visual formats

| Server | Pypi package | Primary formats | Typical tools |
|--------|-------------|-----------------|---------------|
| `aspose-imaging` | aspose-imaging-python-net | PNG, JPEG, TIFF, BMP, WebP, GIF, ICO | convert, resize, crop, rotate, filter, draw |
| `aspose-ocr` | aspose-ocr-python-net | JPG, PNG, TIFF, PDF (scan) | recognize text, detect layout, extract tables |
| `aspose-barcode` | aspose-barcode-for-python-via-net | QR, Code128, EAN, DataMatrix, PDF417 | generate, recognize, decode |
| `aspose-psd` | aspose-psd | PSD, PSB | read layers, export, convert |
| `aspose-svg` | aspose-svg-net | SVG | convert, optimize, render |

### Engineering and technical formats

| Server | Pypi package | Primary formats | Typical tools |
|--------|-------------|-----------------|---------------|
| `aspose-cad` | aspose-cad | DWG, DXF, DWF, DGN, IFC, STL | convert, render, extract entities |
| `aspose-3d` | aspose-3d | FBX, OBJ, STL, GLTF, U3D, DAE | convert, transform, render |
| `aspose-diagram` | aspose-diagram-python | VSD, VSDX, VSX, VTX | convert, extract shapes/text, export |
| `aspose-tasks` | aspose-tasks | MPP, MPT, MPD | read, write, convert, resource planning |
| `aspose-page` | aspose-page | XPS, EPS, PS | convert, merge |

### Web and markup formats

| Server | Pypi package | Primary formats | Typical tools |
|--------|-------------|-----------------|---------------|
| `aspose-html` | aspose-html-net | HTML, MHTML, MD | convert to PDF/image, render, parse |
| `aspose-tex` | aspose-tex-net | TeX, LaTeX | typeset, convert to PDF/image/XPS |

### Archive and financial formats

| Server | Pypi package | Primary formats | Typical tools |
|--------|-------------|-----------------|---------------|
| `aspose-zip` | aspose-zip | ZIP, RAR, 7z, TAR, GZ | create, extract, list, compress, encrypt |
| `aspose-finance` | aspose-finance | XBRL, iXBRL, OFX | read, validate, convert financial reports |

---

## Tool naming conventions

Tools follow a consistent `verb_noun` pattern:

| Prefix | Meaning |
|--------|---------|
| `convert_to_*` | Format conversion (e.g. `convert_to_pdf`, `convert_to_png`) |
| `get_*` | Read metadata or content without modifying the file |
| `extract_*` | Pull specific content out (text, images, attachments) |
| `merge_*` | Combine multiple files into one |
| `split_*` | Divide one file into multiple |
| `add_*` / `insert_*` | Add content to an existing file |
| `remove_*` / `delete_*` | Remove content from an existing file |
| `create_*` | Create a new file |
| `recognize_*` | OCR / barcode recognition |
| `generate_*` | Generate a new artifact (barcode image, QR code) |
| `protect_*` / `encrypt_*` | Apply password or permissions |

---

## Key constraints for reasoning

- **Index convention:** page numbers, slide indices, row/column indices are **0-based**
  unless a tool's description explicitly states otherwise.
- **Output filenames:** many tools have an optional `output_filename` parameter. When
  omitted, the server generates a name automatically. Always report the actual output
  filename from the tool result to the user.
- **Evaluation mode:** without a valid `ASPOSE_LICENSE_FILE`, tools succeed but output
  is watermarked or limited. This is not an error — it is expected behavior.
- **Format enum values:** tools that accept a format string (e.g. `save_format`) require
  the exact enum value as documented (e.g. `"Pdf"`, `"Png"`) — not lowercased variants.
- **File existence:** tools do not create `ASPOSE_FILES_PATH` or download files. The
  input file must already exist in that directory before a tool is called.

---

## Decision logic for routing

```
Incoming file extension → server
.docx .doc .rtf .odt .md  → aspose-words
.pdf                       → aspose-pdf
.xlsx .xls .csv .ods       → aspose-cells
.pptx .ppt .odp            → aspose-slides
.msg .eml .pst .mbox       → aspose-email
.png .jpg .jpeg .tiff .bmp .gif .webp → aspose-imaging
.psd .psb                  → aspose-psd
.svg                       → aspose-svg
.html .mhtml               → aspose-html
.tex                       → aspose-tex
.xps .eps .ps              → aspose-page
.dwg .dxf .dwf             → aspose-cad
.fbx .obj .stl .gltf       → aspose-3d
.vsd .vsdx                 → aspose-diagram
.mpp .mpt                  → aspose-tasks
.zip .rar .7z .tar .gz     → aspose-zip
.xbrl .ixbrl               → aspose-finance
scanned image / photo      → aspose-ocr
barcode / QR task          → aspose-barcode
```

When the task involves converting format A to format B, use the server that owns format A.

---

## What these servers cannot do

- Access the internet or external APIs
- Read files outside `ASPOSE_FILES_PATH`
- Write files outside `ASPOSE_FILES_PATH`
- Accept binary data directly in tool parameters
- Process a format that belongs to a different server
- Operate without the product's Python package installed in its venv
