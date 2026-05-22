# Aspose 3D MCP Server (Standalone)

Standalone MCP server for Aspose.3D for Python via .NET.
Create, load, convert, and manipulate 3D scenes in 20+ formats.
No 3D modeling or rendering software required.

## Package Note

The PyPI package is `aspose-3d` but the Python module is `aspose.threed`
(Python identifiers cannot start with a digit).

```python
# CORRECT
import aspose.threed as a3d
from aspose.threed import Scene, FileFormat

# WRONG — SyntaxError
import aspose.3d
from aspose.3d import Scene
```

## Platform Support

✓ Windows x32/x64
✓ Linux (Ubuntu, CentOS, and others)
✓ macOS

This is a fully cross-platform server.

## Supported 3D Formats

**Input & Output:** OBJ, STL, glTF, GLB, 3MF, COLLADA (DAE), VRML
**Partial import:** FBX (tokenizer only — not recommended as production source format)
**Input only:** 3DS, USD, USDZ, DXF, RVM, JT, ASE, X
**Output only:** HTML5 (3D viewer), PDF (3D embedded)

## Quick Setup

### 1. Create your .env file
```bash
cp .env.example .env
# Edit .env and set your folder paths
```

### 2. Create the virtual environment

**Linux/macOS:**
```bash
bash servers/threed/setup_venv.sh
source servers/threed/.venv/bin/activate
```

**Windows:**
```batch
servers\threed\setup_venv.bat
servers\threed\.venv\Scripts\activate.bat
```

### 3. Start the server
```bash
# stdio
python servers/threed/server.py

# HTTP mode (port 8007)
python servers/threed/server.py --transport streamable-http --port 8007

# SSE legacy
python servers/threed/server.py --transport sse --port 8007
```

## Available Tools

- `threed_convert` — Convert any supported 3D file to another format
- `threed_convert_to_stl` — Convert to STL (3D printing)
- `threed_convert_to_obj` — Convert to OBJ/Wavefront
- `threed_convert_to_gltf` — Convert to glTF 2.0
- `threed_convert_to_glb` — Convert to GLB (binary glTF)
- `threed_convert_to_3mf` — Convert to 3MF (3D printing, richer than STL)
- `threed_convert_to_pdf` — Embed 3D scene in PDF
- `threed_convert_to_html` — Export as interactive HTML5 viewer
- `threed_convert_to_collada` — Convert to COLLADA/DAE
- `threed_create_scene` — Create 3D scene with primitives (box, cylinder, sphere)
- `threed_get_scene_info` — Get node count, child node names of a 3D file
- `threed_detect_format` — Detect the format of a 3D file
- `threed_merge_scenes` — Merge two 3D files into one scene

## Host Configuration

See `docs/host-setup/` for ready-to-use JSON configs for Claude Desktop, VS Code,
Cursor, Cline, streamable-http, and SSE.
