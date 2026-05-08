<div align="center">

# Canada Aida Ai MCP

**MCP server for canada aida ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-canada-aida-ai-mcp)](https://pypi.org/project/meok-canada-aida-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Canada Aida Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `classify_ai_system` | Classify an AI system under AIDA as high-impact or general-purpose. |
| `impact_assessment` | Perform an AI impact assessment per AIDA requirements (Sections 7-8). |
| `compliance_check` | Check compliance with AIDA obligations. Evaluates whether a responsible |
| `crosswalk_to_eu_ai_act` | Map AIDA requirements to EU AI Act obligations. Essential for |
| `generate_documentation` | Generate AIDA compliance documentation including public system |

## Installation

```bash
pip install meok-canada-aida-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "canada-aida-ai-mcp": {
      "command": "python",
      "args": ["-m", "meok_canada_aida_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
