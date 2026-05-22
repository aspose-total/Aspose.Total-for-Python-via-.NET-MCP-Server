# Aspose TeX MCP Server (Standalone)

Standalone MCP server exposing Aspose.TeX for Python via .NET tools.
Converts TeX/LaTeX files to PDF, PNG, JPEG, BMP, TIFF, XPS, and SVG.
Also renders LaTeX math formulas and figures to PNG/SVG images.

## ⚠️ Platform Requirement

**Windows only (x86/x64).** The `aspose-tex-net` package has no Linux or macOS wheels.
This server can be installed and started on any platform, but all TeX tools will return
an error on non-Windows systems. Run this server on Windows.

## Quick Setup (Windows)

### 1. Create your .env file

```batch
copy .env.example .env
REM Edit .env and set your folder paths
```

### 2. Create and activate the virtual environment

```batch
servers\tex\setup_venv.bat
servers\tex\.venv\Scripts\activate.bat
```

### 3. Start the server

```batch
python servers\tex\server.py
python servers\tex\server.py --transport streamable-http --port 8002
```

## Host Configuration

See [docs/host-setup/](docs/host-setup/) for ready-to-use config files for each MCP host.

## Available Tools

| Tool | Description |
|------|-------------|
| `tex_convert_to_pdf` | Convert LaTeX file to PDF |
| `tex_convert_to_png` | Convert LaTeX file to PNG image(s) |
| `tex_convert_to_jpeg` | Convert LaTeX file to JPEG image(s) |
| `tex_convert_to_bmp` | Convert LaTeX file to BMP image(s) |
| `tex_convert_to_tiff` | Convert LaTeX file to TIFF image(s) |
| `tex_convert_to_xps` | Convert LaTeX file to XPS |
| `tex_convert_to_svg` | Convert LaTeX file to SVG |
| `tex_render_math_to_png` | Render LaTeX math formula to PNG |
| `tex_render_math_to_svg` | Render LaTeX math formula to SVG |
| `tex_render_figure_to_png` | Render LaTeX figure to PNG |
| `tex_render_figure_to_svg` | Render LaTeX figure to SVG |

## Package Note

This server uses `aspose-tex-net` — note the `-net` suffix. The package `aspose-tex` is
a different (non-existent) package. Always use the full `aspose-tex-net` name.

## Linux / macOS

Running `setup_venv.sh` on Linux or macOS will fail with a pip error because
`aspose-tex-net` has no wheels for those platforms. This is expected.
The server must run on Windows.
