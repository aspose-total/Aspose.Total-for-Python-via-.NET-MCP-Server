# Aspose CAD MCP Server (Standalone)

Standalone MCP server for Aspose.CAD for Python via .NET.
Process AutoCAD DWG/DXF, BIM IFC, and 20+ other CAD/BIM formats.
No AutoCAD or other CAD software required.

## Platform Support

✅ Windows x32/x64
✅ Linux (Ubuntu, CentOS, OpenSUSE, and others)
✅ macOS

This is a fully cross-platform server.

## Python Version Requirement

⚠️ **aspose-cad requires Python >= 3.9.**
If you are using Python 3.8 or earlier, the package may not install correctly.
Use Python 3.9 or later.

## Quick Setup

### 1. Verify Python version
```bash
python --version   # Must be >= 3.9
```

### 2. Create your .env file
```bash
cp .env.example .env
# Edit .env and set your folder paths
```

### 3. Create the virtual environment

**Linux/macOS:**
```bash
bash servers/cad/setup_venv.sh
source servers/cad/.venv/bin/activate
```

**Windows:**
```batch
servers\cad\setup_venv.bat
servers\cad\.venv\Scripts\activate.bat
```

### 4. Start the server
```bash
# stdio
python servers/cad/server.py

# HTTP mode (port 8008)
python servers/cad/server.py --transport streamable-http --port 8008

# SSE legacy
python servers/cad/server.py --transport sse --port 8008
```

## Key Concept: Rasterization Options

Every CAD-to-image/PDF conversion requires two objects:
1. `CadRasterizationOptions` — defines page size, layers, layouts
2. A format options object (`PdfOptions`, `PngOptions`, etc.) with
   `vector_rasterization_options` set to the rasterization options

All tools handle this automatically. Just pass the input filename and output format.

## Supported Input Formats

**AutoCAD:** DWG, DWT, DXF
**MicroStation:** DGN
**BIM:** IFC
**Other:** DWF, DWFx, STL, IGES (IGS), CF2, OBJ, PLT, HPGL, DXB, 3DS, U3D,
COLLADA (DAE), STP/STEP, FBX, GLB, GLTF, CGM, DRACO (DRC)

## Supported Output Formats

**Fixed Layout:** PDF
**Vector Images:** SVG, WMF, EMF
**Raster Images:** PNG, BMP, TIFF, JPEG, GIF

## Available Tools

- `cad_convert_to_pdf` — Convert CAD/BIM drawing to PDF
- `cad_convert_to_png` — Convert CAD/BIM drawing to PNG image
- `cad_convert_to_jpeg` — Convert CAD/BIM drawing to JPEG image
- `cad_convert_to_bmp` — Convert CAD/BIM drawing to BMP image
- `cad_convert_to_tiff` — Convert CAD/BIM drawing to TIFF image
- `cad_convert_to_svg` — Convert CAD/BIM drawing to SVG vector image
- `cad_convert_to_gif` — Convert CAD/BIM drawing to GIF image
- `cad_get_drawing_info` — Get dimensions and type info of CAD file
- `cad_export_layer_to_pdf` — Export specific layer(s) to PDF
- `cad_export_layout_to_pdf` — Export specific layout(s) to PDF
- `cad_export_layer_to_png` — Export specific layer(s) to PNG

## Host Configuration

See `docs/host-setup/` for ready-to-use JSON configs for Claude Desktop, VS Code, Cursor, and more.
