# Aspose SVG MCP Server (Standalone)

Standalone MCP server exposing Aspose.SVG for Python via .NET tools.
Create, edit, convert, and vectorize SVG documents.
Convert SVG to PDF, PNG, JPEG, BMP, GIF, TIFF, and XPS.
Vectorize raster images (PNG, JPEG, BMP, GIF, TIFF) to SVG.

## ⚠️ Platform Requirement

**Windows only (x86/x64).** The `aspose-svg-net` package has no Linux or macOS wheels.
This server can be installed and started on any platform, but all SVG tools will return
an error on non-Windows systems. Run this server on Windows.

## Quick Setup (Windows)

### 1. Create your .env file

```batch
copy .env.example .env
REM Edit .env and set your folder paths
```

### 2. Create and activate the virtual environment

```batch
servers\svg\setup_venv.bat
servers\svg\.venv\Scripts\activate.bat
```

### 3. Start the server

```batch
python servers\svg\server.py
python servers\svg\server.py --transport streamable-http --port 8003
```

## Host Configuration

See [docs/host-setup/](docs/host-setup/) for ready-to-use config files for each MCP host.

## Available Tools

| Tool | Description |
|------|-------------|
| `svg_convert_to_pdf` | Convert SVG file to PDF |
| `svg_convert_to_png` | Convert SVG file to PNG image |
| `svg_convert_to_jpeg` | Convert SVG file to JPEG image |
| `svg_convert_to_bmp` | Convert SVG file to BMP image |
| `svg_convert_to_gif` | Convert SVG file to GIF image |
| `svg_convert_to_tiff` | Convert SVG file to TIFF image |
| `svg_convert_to_xps` | Convert SVG file to XPS |
| `svg_create_document` | Create SVG document from SVG string content |
| `svg_get_document_info` | Get SVG dimensions, element count, title |
| `svg_add_element` | Add a shape element to an existing SVG |
| `svg_query_elements` | Query SVG elements by CSS selector |
| `svg_extract_text` | Extract all text content from SVG |
| `svg_vectorize_image` | Convert raster image (PNG/JPEG/BMP) to SVG |
| `svg_merge_to_pdf` | Merge multiple SVG files into one PDF |

## Package Note

This server uses `aspose-svg-net` — note the `-net` suffix. The package `aspose-svg` does
not exist. Always use the full `aspose-svg-net` name.

## Linux / macOS

Running `setup_venv.sh` on Linux or macOS will fail with a pip error because
`aspose-svg-net` has no wheels for those platforms. This is expected.
The server must run on Windows.
