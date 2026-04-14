# Canada AIDA (Artificial Intelligence and Data Act) Compliance MCP Server

> **By [MEOK AI Labs](https://meok.ai)** -- Sovereign AI tools for everyone.

Compliance assessment for Canada's Artificial Intelligence and Data Act (AIDA), Part 3 of Bill C-27. Classify AI systems (high-impact/general), perform impact assessments, check compliance obligations, crosswalk to EU AI Act, and generate compliance documentation.

Part of the **CSOAI Governance Suite**: AIDA + EU AI Act + GDPR + ISO 42001 + NIST AI RMF.

[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-255+_servers-purple)](https://meok.ai)

## Tools

| Tool | Description |
|------|-------------|
| `classify_ai_system` | Classify AI system as high-impact or general under AIDA |
| `impact_assessment` | AI impact assessment per AIDA Sections 7-8 |
| `compliance_check` | Check compliance with all AIDA obligations |
| `crosswalk_to_eu_ai_act` | Map AIDA requirements to EU AI Act |
| `generate_documentation` | Generate AIDA compliance documents (public descriptions, records, notifications) |

## Quick Start

```bash
pip install mcp
git clone https://github.com/CSOAI-ORG/canada-aida-ai-mcp.git
cd canada-aida-ai-mcp
python server.py
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "canada-aida-ai": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/canada-aida-ai-mcp"
    }
  }
}
```

## Coverage

- **All AIDA sections** (5-12) with obligation mapping
- **6 high-impact criteria** (health/safety, human rights, economic, vulnerable populations, scale, bias)
- **10 AIDA-to-EU AI Act crosswalk mappings** with alignment analysis
- **4 document templates** (public description, compliance records, affected person notification, Minister notification)
- **Penalty exposure assessment** (up to $25M or 5% global revenue)

## The Canadian Market

AIDA is Canada's answer to the EU AI Act. This server provides the first MCP-accessible compliance tool for Canadian AI regulation, essential for organizations deploying AI in the Canadian market.

## License

MIT -- see [LICENSE](LICENSE)
