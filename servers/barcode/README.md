# Aspose BarCode MCP Server (Standalone)

Standalone MCP server exposing Aspose.BarCode for Python via .NET tools.
Generates and recognises 60+ barcode symbologies including QR, DataMatrix,
Code128, EAN-13, PDF417, Aztec, and more.

## Quick Setup

### 1. Create your .env file
```
cp .env.example .env
# Edit .env and set your folder paths
```

### 2. Create and activate the virtual environment

**Linux / macOS:**
```
bash servers/barcode/setup_venv.sh
source servers/barcode/.venv/bin/activate
```

**Windows:**
```
servers\barcode\setup_venv.bat
servers\barcode\.venv\Scripts\activate.bat
```

### 3. Start the server
```
python servers/barcode/server.py                                           # stdio
python servers/barcode/server.py --transport streamable-http --port 8001  # HTTP
```

## Host Configuration

See [docs/host-setup/](docs/host-setup/) for ready-to-use config files for each MCP host.

## Available Tools

| Tool | Description |
|------|-------------|
| `barcode_generate` | Generate any barcode symbology by name |
| `barcode_generate_qr` | Generate QR code (convenience tool) |
| `barcode_generate_datamatrix` | Generate DataMatrix barcode |
| `barcode_generate_pdf417` | Generate PDF417 barcode |
| `barcode_generate_ean13` | Generate EAN-13 barcode |
| `barcode_generate_code128` | Generate Code128 barcode |
| `barcode_generate_custom` | Generate barcode with custom appearance |
| `barcode_generate_svg` | Generate barcode as SVG vector image |
| `barcode_recognize_all` | Recognise all barcodes in an image |
| `barcode_recognize_type` | Recognise specific barcode type |
| `barcode_recognize_with_regions` | Recognise barcodes and return bounding boxes |
| `barcode_recognize_multiple_types` | Recognise multiple specific symbologies |
| `barcode_list_symbologies` | List all supported generation symbology names |
| `barcode_get_image_format_names` | List supported output image format names |

## Package Note

This server uses `aspose-barcode-for-python-via-net` — the unusually long package name
is intentional. The short variant `aspose-barcode` is a different product with a
different API. Always use the full name.
