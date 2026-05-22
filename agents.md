# Aspose MCP Servers — Agent Guide

This guide is for AI agents (Claude, Cursor, Cline, Copilot, etc.) connected to one or
more Aspose MCP servers. It describes how to use the tools correctly, how to chain
operations, and how to recover from common errors.

---

## Core rules — read these first

1. **Bare filenames only.** Every tool that accepts a file path takes a bare filename
   (e.g. `report.docx`), never a full path. The server resolves the full path internally
   using `ASPOSE_FILES_PATH`. Passing a full path will always fail.

2. **Input files must already exist in `ASPOSE_FILES_PATH`.**  
   Before calling any tool, confirm the input file is in the server's files directory.
   If the user refers to a file somewhere else on their machine, ask them to copy it there
   first — you cannot move files between directories yourself.

3. **Output files are written to the same `ASPOSE_FILES_PATH` directory.**  
   After a conversion or export tool runs, the output file is in the same folder as the
   input. You can chain tools by using the output filename as the next tool's input.

4. **Each product is a separate MCP server.**  
   `aspose-words`, `aspose-pdf`, `aspose-cells`, etc. are distinct servers. A tool from
   `aspose-words` cannot process a PDF — use `aspose-pdf` for that. Match the file type
   to the correct server before calling any tool.

5. **One server per product — no cross-server tool calls in a single step.**  
   You can chain across servers (output of one becomes input of the next), but each tool
   call goes to exactly one server.

---

## Choosing the right server

| File type / task | Server to use |
|-----------------|---------------|
| DOCX, DOC, RTF, ODT | `aspose-words` |
| PDF | `aspose-pdf` |
| XLSX, XLS, CSV, ODS | `aspose-cells` |
| PPTX, PPT, ODP | `aspose-slides` |
| MSG, EML, PST, MBOX | `aspose-email` |
| Images (PNG, JPEG, TIFF, BMP, WebP, SVG) | `aspose-imaging` |
| Scanned documents / OCR | `aspose-ocr` |
| Barcodes / QR codes | `aspose-barcode` |
| ZIP, RAR, 7z, TAR | `aspose-zip` |
| HTML files | `aspose-html` |
| PSD / PSB (Photoshop) | `aspose-psd` |
| SVG files | `aspose-svg` |
| TeX / LaTeX | `aspose-tex` |
| XPS, EPS, PS | `aspose-page` |
| DWG, DXF, DWF (CAD) | `aspose-cad` |
| FBX, OBJ, STL, GLTF (3D) | `aspose-3d` |
| MPP, MPT (MS Project) | `aspose-tasks` |
| VSD, VSDX (Visio) | `aspose-diagram` |
| XBRL, iXBRL (finance) | `aspose-finance` |

When a user asks to "convert X to Y", identify both the source format and target format,
pick the server that owns the source format, then call the appropriate conversion tool.

---

## Tool call patterns

### Single-step: convert a file

```
User: Convert report.docx to PDF

→ Call: aspose-words / convert_to_pdf
    input_filename: "report.docx"
    output_filename: "report.pdf"   (or let the tool auto-name it)
→ Report: "report.pdf has been saved to your files directory."
```

### Multi-step: chain across servers

```
User: Extract text from scan.jpg and save it as a Word document

Step 1 → aspose-ocr / recognize_image
    input_filename: "scan.jpg"
    output_filename: "scan.txt"

Step 2 → aspose-words / create_document_from_text  (or similar)
    input_filename: "scan.txt"
    output_filename: "scan.docx"

→ Report both steps and the final filename.
```

### Read / inspect before modifying

Always prefer reading metadata or content before making destructive changes:

```
User: Remove the second page from report.pdf

Step 1 → aspose-pdf / get_page_count   ← verify the file has at least 2 pages
Step 2 → aspose-pdf / remove_page
    input_filename: "report.pdf"
    page_index: 1                       ← 0-based index
```

---

## Parameter conventions

| Convention | Details |
|------------|---------|
| **File parameters** | Always bare filename — `"invoice.pdf"` not `"C:/files/invoice.pdf"` |
| **Page indices** | 0-based unless a tool's description says otherwise |
| **Output filename** | If optional, omit it — the server generates a sensible default |
| **Format strings** | Use the tool's documented enum values exactly (e.g. `"Png"` not `"png"`) |

---

## Error handling

| Error | What it means | What to do |
|-------|--------------|------------|
| `ASPOSE_FILES_PATH is not configured` | Server misconfiguration | Tell the user to check their MCP host config — the env var is missing |
| `File not found: foo.docx` | File not in the files directory | Ask the user to copy the file to their `ASPOSE_FILES_PATH` folder |
| `health_check failed` | Aspose package not installed in this server's venv | Tell the user to re-run `setup_venv.bat` for this product |
| Tool returns watermark warning | No license active | Inform the user — output is usable but watermarked in evaluation mode |
| Unexpected format error | Wrong server for this file type | Check the file extension and route to the correct server |

---

## Common workflows

### Extract all text from a scanned PDF

```
1. aspose-pdf / extract_images → saves page images to ASPOSE_FILES_PATH
2. aspose-ocr / recognize_image → for each image, extract text
3. Concatenate results and present to user (or write to a .txt file)
```

### Merge multiple Word documents

```
1. Confirm all source .docx files are in ASPOSE_FILES_PATH
2. aspose-words / merge_documents
   source_filenames: ["part1.docx", "part2.docx", "part3.docx"]
   output_filename: "merged.docx"
```

### Read a spreadsheet and summarize data

```
1. aspose-cells / read_worksheet → returns cell data as structured output
2. Summarize / analyze the returned data yourself (no second tool call needed)
```

### Generate a barcode and embed it in a Word document

```
1. aspose-barcode / generate_barcode
   data: "https://example.com"
   format: "QR"
   output_filename: "qr.png"
2. aspose-words / insert_image
   document_filename: "template.docx"
   image_filename: "qr.png"
   output_filename: "template_with_qr.docx"
```

---

## Things to avoid

- **Do not guess tool names.** Use only tools that appear in the server's tool list.
- **Do not pass directory paths as filenames.** `"docs/report.pdf"` will fail — use `"report.pdf"`.
- **Do not assume a tool exists on every server.** Each server only exposes tools for its own product.
- **Do not call tools on a server that is not connected.** Check which servers are active before planning a multi-step workflow.
