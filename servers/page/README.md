# Aspose Page MCP Server (Standalone)

Standalone MCP server for Aspose.Page for Python via .NET.
Process XPS/OXPS documents and PS/EPS/AI PostScript files.
Convert to PDF and raster images (PNG, JPEG, BMP, TIFF).
Create and edit XPS documents programmatically.

## WARNING: Platform Requirement (Windows only)

**Windows only (x86/x64).** The `aspose-page` package has no Linux or macOS wheels.
The server starts on any platform but all Page tools will fail on non-Windows systems.

## Quick Setup (Windows)

1. Copy `.env.example` to `.env` and set your folder path
2. Run: `servers\page\setup_venv.bat`
3. Activate: `servers\page\.venv\Scripts\activate.bat`
4. Start: `python servers\page\server.py`
5. HTTP mode: `python servers\page\server.py --transport streamable-http --port 8005`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ASPOSE_FILES_PATH` | Folder for input and output files |
| `ASPOSE_LICENSE_FILE` | Path to Aspose.Total.lic (optional) |

## Host Configuration

See `docs/host-setup/` for ready-to-use JSON configs for Claude Desktop, VS Code,
Cursor, Cline, and HTTP transports.

## Available Tools

| Tool | Description |
|------|-------------|
| `page_xps_to_pdf` | Convert XPS/OXPS file to PDF |
| `page_xps_to_png` | Convert XPS/OXPS file to PNG images (one per page) |
| `page_xps_to_jpeg` | Convert XPS/OXPS file to JPEG images |
| `page_xps_to_bmp` | Convert XPS/OXPS file to BMP images |
| `page_xps_to_tiff` | Convert XPS/OXPS file to TIFF images |
| `page_ps_to_pdf` | Convert PS/EPS file to PDF |
| `page_ps_to_png` | Convert PS/EPS file to PNG images |
| `page_ps_to_jpeg` | Convert PS/EPS file to JPEG images |
| `page_eps_to_png` | Convert EPS file to PNG (convenience alias) |
| `page_create_xps` | Create new XPS document with text content |
| `page_get_xps_info` | Get page count and properties of XPS file |
| `page_merge_xps` | Merge multiple XPS files into one |

## Supported Formats

**Input:** XPS, OXPS, PS (PostScript), EPS, AI (Adobe Illustrator)
**Output:** PDF, PNG, JPEG, BMP, TIFF, XPS
