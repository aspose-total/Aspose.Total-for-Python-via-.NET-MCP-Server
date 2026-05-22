# Aspose PSD MCP Server (Standalone)

Standalone MCP server for Aspose.PSD for Python via .NET.
Process Adobe Photoshop PSD/PSB files and Adobe Illustrator AI files without
installing Photoshop or Illustrator.

## Platform Support

✅ Windows x32/x64
✅ Linux x64
✅ macOS x64/Arm64

This is a fully cross-platform server — no platform restrictions.

## Quick Setup

### 1. Create your .env file

```bash
cp .env.example .env
# Edit .env and set your folder paths
```

### 2. Create the virtual environment

**Linux/macOS:**

```bash
bash servers/psd/setup_venv.sh
source servers/psd/.venv/bin/activate
```

**Windows:**

```batch
servers\psd\setup_venv.bat
servers\psd\.venv\Scripts\activate.bat
```

### 3. Start the server

```bash
# stdio (for MCP host integration)
python servers/psd/server.py

# HTTP mode (port 8004)
python servers/psd/server.py --transport streamable-http --port 8004

# SSE legacy
python servers/psd/server.py --transport sse --port 8004
```

## Available Tools

- `psd_convert_to_png` — Export PSD to PNG with transparency
- `psd_convert_to_jpeg` — Export PSD to JPEG
- `psd_convert_to_tiff` — Export PSD to TIFF
- `psd_convert_to_bmp` — Export PSD to BMP
- `psd_convert_to_gif` — Export PSD to GIF
- `psd_convert_to_pdf` — Export PSD to PDF
- `psd_get_document_info` — Get PSD dimensions, layer count, color mode
- `psd_list_layers` — List all layers with names, types, and visibility
- `psd_update_text_layer` — Update a text layer by name or index
- `psd_flatten_image` — Flatten all layers into one and export
- `psd_resize` — Resize the PSD canvas
- `psd_crop` — Crop the PSD canvas
- `psd_rotate` — Rotate the PSD image
- `psd_add_text_watermark` — Add text watermark via Graphics API

## Package

**PyPI package:** `aspose-psd` (simple name — no `-net` suffix)

```bash
pip install aspose-psd
```

## Host Configuration

See `docs/host-setup/` for ready-to-use config files for Claude Desktop, VS Code,
Cursor, Cline, streamable-http, and SSE.
