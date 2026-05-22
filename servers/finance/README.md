# Aspose Finance MCP Server (Standalone)

Standalone MCP server for Aspose.Finance for Python via .NET.
Process XBRL, iXBRL, and OFX financial document formats.
Create, read, validate, and convert financial reporting documents.

## Platform Support

✅ Windows x32/x64
✅ Linux (Ubuntu, OpenSUSE, CentOS, and others)
✅ Unix/macOS

This is a fully cross-platform server — no platform restrictions.

## Python Version Requirement

⚠️ **aspose-finance requires Python >=3.5 and <3.12.**
If you are using Python 3.12 or later, the package will not install.
Use Python 3.11 or earlier.

## Quick Setup

### 1. Verify Python version
```bash
python --version   # Must be 3.5 ≤ version < 3.12
```

### 2. Create your .env file
```bash
cp .env.example .env
# Edit .env and set your folder paths
```

### 3. Create the virtual environment

**Linux/macOS:**
```bash
bash servers/finance/setup_venv.sh
source servers/finance/.venv/bin/activate
```

**Windows:**
```batch
servers\finance\setup_venv.bat
servers\finance\.venv\Scripts\activate.bat
```

### 4. Start the server
```bash
# stdio (for MCP host integration)
python servers/finance/server.py

# HTTP mode (port 8006)
python servers/finance/server.py --transport streamable-http --port 8006

# SSE legacy
python servers/finance/server.py --transport sse --port 8006
```

## Available Tools

- `finance_create_xbrl` — Create a new empty XBRL instance document
- `finance_read_xbrl` — Read XBRL and return instance info
- `finance_validate_xbrl` — Validate XBRL instance(s) and return errors
- `finance_xbrl_to_xlsx` — Convert XBRL to Excel XLSX
- `finance_xbrl_to_ixbrl` — Convert XBRL to iXBRL (inline XBRL)
- `finance_read_ixbrl` — Read iXBRL document info
- `finance_validate_ixbrl` — Validate iXBRL document
- `finance_ixbrl_to_xlsx` — Convert iXBRL to Excel XLSX
- `finance_ofx_request_to_v2` — Convert OFX request 1.x (SGML) → 2.x (XML)
- `finance_ofx_request_to_v1` — Convert OFX request 2.x (XML) → 1.x (SGML)
- `finance_ofx_response_to_v2` — Convert OFX response 1.x (SGML) → 2.x (XML)
- `finance_ofx_response_to_v1` — Convert OFX response 2.x (XML) → 1.x (SGML)

## Host Configuration
See `docs/host-setup/` for ready-to-use JSON configs.
