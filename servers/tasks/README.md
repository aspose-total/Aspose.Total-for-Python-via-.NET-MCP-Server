# Aspose Tasks MCP Server (Standalone)

Standalone MCP server for Aspose.Tasks for Python via .NET.
Read, create, convert, and manipulate Microsoft Project MPP/MPX files,
Oracle Primavera XER files, and project XML files without MS Project.

## Platform Support

✓ Windows x32/x64
✓ Linux (Ubuntu, CentOS, and others)
✓ macOS

This is a fully cross-platform server.

## Quick Setup

### 1. Create your .env file

```bash
cp .env.example .env
# Edit .env and set your folder paths
```

### 2. Create the virtual environment

**Linux/macOS:**
```bash
bash servers/tasks/setup_venv.sh
source servers/tasks/.venv/bin/activate
```

**Windows:**
```batch
servers\tasks\setup_venv.bat
servers\tasks\.venv\Scripts\activate.bat
```

### 3. Start the server

```bash
python servers/tasks/server.py                                  # stdio
python servers/tasks/server.py --transport streamable-http --port 8009  # HTTP
python servers/tasks/server.py --transport sse --port 8009     # SSE
```

## Save Pattern Note

Aspose.Tasks uses two different save patterns:

- **Document formats** (PDF, HTML, XLSX, CSV, XML, MPP, MPX, XPS, TXT):
  `prj.save("output.pdf", SaveFileFormat.PDF)`
- **Image formats** (PNG, JPEG, BMP, TIFF, SVG):
  `options = ImageSaveOptions(SaveFileFormat.PNG); prj.save("output.png", options)`

All tools handle this automatically.

## Available Tools

- `tasks_convert_to_pdf` — Convert project to PDF
- `tasks_convert_to_png` — Export project as PNG image
- `tasks_convert_to_jpeg` — Export project as JPEG image
- `tasks_convert_to_svg` — Export project as SVG
- `tasks_convert_to_xlsx` — Convert project to Excel XLSX
- `tasks_convert_to_html` — Convert project to HTML
- `tasks_convert_to_xml` — Convert project to XML (MS Project format)
- `tasks_convert_to_csv` — Convert project to CSV
- `tasks_convert_to_mpx` — Convert project to MPX format
- `tasks_get_project_info` — Get task count, resource count, dates
- `tasks_list_tasks` — List all tasks with name, start, finish, duration
- `tasks_list_resources` — List all project resources
- `tasks_create_project` — Create a new project with initial tasks
