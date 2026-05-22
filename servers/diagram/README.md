# Aspose Diagram MCP Server (Standalone)

Standalone MCP server for Aspose.Diagram for Python via .NET.
Process Microsoft Visio VSDX/VSD diagrams without installing Visio.
Convert to PDF, PNG, JPEG, SVG, HTML, and other formats.

## ⚠️ Package Name Warning

Use **`aspose-diagram-python`** (`pip install aspose-diagram-python`).

**Do NOT use:**
- `aspose-diagram` — this is the Python via **Java** variant requiring a JVM (jpype/JPype).
  It uses a completely different import: `import jpype; from asposediagram.api import *`
  and will **not work** with this server.
- `aspose-diagram-cloud` — this requires Aspose Cloud API credentials and is a REST SDK,
  not a local processing library.

The correct import is: `import aspose.diagram` (from `aspose-diagram-python`).

## Platform Support

✓ Windows x32/x64
✓ Linux (Ubuntu, CentOS, and others)
✓ macOS

Fully cross-platform — no platform restrictions.

## Quick Setup

### 1. Create your .env file

```bash
cp .env.example .env
# Edit .env and set your folder paths
```

### 2. Create the virtual environment

**Linux/macOS:**
```bash
bash servers/diagram/setup_venv.sh
source servers/diagram/.venv/bin/activate
```

**Windows:**
```batch
servers\diagram\setup_venv.bat
servers\diagram\.venv\Scripts\activate.bat
```

### 3. Start the server

```bash
python servers/diagram/server.py                                   # stdio
python servers/diagram/server.py --transport streamable-http --port 8010  # HTTP
python servers/diagram/server.py --transport sse --port 8010      # SSE
```

## Image Format Note

Aspose.Diagram requires `ImageSaveOptions` for raster image formats (PNG, JPEG, SVG, TIFF).
This is handled automatically by all image conversion tools.

```python
from aspose.diagram import Diagram, SaveFileFormat
from aspose.diagram import saving

diagram = Diagram("input.vsdx")
options = saving.ImageSaveOptions(SaveFileFormat.PNG)
options.page_index = 0
diagram.save("output.png", options)
```

For document formats (PDF, XPS, VSDX), `SaveFileFormat` is used directly:
```python
diagram.save("output.pdf", SaveFileFormat.PDF)
```

## Available Tools

- `diagram_convert_to_pdf` — Convert Visio diagram to PDF
- `diagram_convert_to_png` — Render Visio diagram to PNG
- `diagram_convert_to_jpeg` — Render Visio diagram to JPEG
- `diagram_convert_to_svg` — Render Visio diagram to SVG
- `diagram_convert_to_tiff` — Render Visio diagram to TIFF
- `diagram_convert_to_html` — Export Visio diagram to HTML
- `diagram_convert_to_xps` — Convert Visio diagram to XPS
- `diagram_convert_to_vsdx` — Convert legacy VSD to modern VSDX
- `diagram_get_diagram_info` — Get page count, shape counts, page names
- `diagram_export_page_to_pdf` — Export a specific page to PDF
- `diagram_export_page_to_png` — Export a specific page to PNG
- `diagram_list_shapes` — List shapes on a specific page
- `diagram_detect_format` — Detect Visio file format
