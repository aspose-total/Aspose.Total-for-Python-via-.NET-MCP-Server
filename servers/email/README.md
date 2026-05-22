# Aspose Email MCP Server (Standalone)

Standalone MCP server for Aspose.Email for Python via .NET.
Read, convert, and process email files without installing any email client.
Supports MSG, EML, MHTML, HTML, PST, MBOX, and other formats.

## ⚠️ Package Name Warning

Use **`aspose-email-for-python-via-net`** (`pip install aspose-email-for-python-via-net`).

This is an unusually long package name — do not truncate it.

**Do NOT use:**
- `aspose-email-cloud` — this requires Aspose Cloud API credentials and is a REST SDK,
  not a local processing library.
- `aspose-email` — this package does not exist as a pip-installable .NET binding.
  Installing it will fail or install the wrong library.

The correct import is: `import aspose.email` (from `aspose-email-for-python-via-net`).

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
bash servers/email/setup_venv.sh
source servers/email/.venv/bin/activate
```

**Windows:**
```batch
servers\email\setup_venv.bat
servers\email\.venv\Scripts\activate.bat
```

### 3. Start the server

```bash
python servers/email/server.py                                   # stdio
python servers/email/server.py --transport streamable-http --port 8011  # HTTP
python servers/email/server.py --transport sse --port 8011      # SSE
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ASPOSE_INPUT_DIR` | Yes | Folder containing input email files |
| `ASPOSE_OUTPUT_DIR` | No | Output folder (falls back to INPUT_DIR) |
| `ASPOSE_LICENSE_PATH` | No | Path to Aspose.Total.lic (evaluation mode if unset) |

## Available Tools

- `email_read_message` — Read an email and return subject, from, to, body, and attachment list
- `email_create_message` — Create a new email message and save to EML or MSG
- `email_convert_to_msg` — Convert an email file to Outlook MSG format
- `email_convert_to_eml` — Convert an email file to EML format
- `email_convert_to_mhtml` — Convert an email file to MHTML format
- `email_convert_to_html` — Convert an email file to HTML format
- `email_extract_attachments` — Extract all attachments from an email to the output folder
- `email_list_headers` — List all MIME headers of an email message
- `email_read_pst_folders` — List folders and message counts in a PST/OST archive
- `email_extract_from_pst` — Extract messages from a PST folder to EML files
- `email_read_mbox` — Read messages from an MBOX archive and return summaries
- `email_detect_format` — Detect the format of an email file
