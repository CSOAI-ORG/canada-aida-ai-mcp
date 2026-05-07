[![canada-aida-ai-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/canada-aida-ai-mcp/badges/card.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/canada-aida-ai-mcp)

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/canada-aida-ai-mcp)](https://pypi.org/project/canada-aida-ai-mcp/)
[![Downloads](https://img.shields.io/pypi/dm/canada-aida-ai-mcp)](https://pypi.org/project/canada-aida-ai-mcp/)
[![GitHub stars](https://img.shields.io/github/stars/CSOAI-ORG/canada-aida-ai-mcp)](https://github.com/CSOAI-ORG/canada-aida-ai-mcp/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

# Canada AIDA MCP

**Artificial Intelligence and Data Act (AIDA) compliance assessment. High-impact AI classification, impact assessments, and regulatory obligation mapping for the Canadian market.**

[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-224+_servers-purple)](https://meok.ai)

[Install](#install) · [Tools](#tools) · [Pricing](#pricing) · [Attestation API](#attestation-api)

</div>

---

## Why This Exists

Canada's Artificial Intelligence and Data Act (AIDA), introduced as Part 3 of Bill C-27, creates obligations for organisations that design, develop, or deploy high-impact AI systems in Canada. While AIDA's timeline has shifted, organisations serving the Canadian market must prepare for high-impact classification, mandatory impact assessments, bias auditing, transparency requirements, and reporting obligations.

AIDA's high-impact AI system classification parallels the EU AI Act's risk tiers, but with distinct Canadian requirements. Companies operating across both jurisdictions need dual compliance coverage. This MCP classifies AI systems under AIDA criteria, performs impact assessments, checks compliance obligations, crosswalks to EU AI Act requirements, and generates the required documentation.

## Install

```bash
pip install canada-aida-ai-mcp
```

## Tools

| Tool | AIDA Reference | What it does |
|------|---------------|--------------|
| `classify_ai_system` | Part 3 (high-impact) | Classify AI system as high-impact under AIDA criteria |
| `impact_assessment` | AIDA Sec. 7-8 | Perform mandatory impact assessment for high-impact systems |
| `compliance_check` | AIDA Sec. 4-13 | Full compliance check against AIDA obligations |
| `crosswalk_to_eu_ai_act` | AIDA + EU AI Act | Map AIDA obligations to EU AI Act requirements |
| `generate_documentation` | AIDA Sec. 11 | Generate transparency and accountability documentation |

## Example

```
Prompt: "Classify our resume screening AI for AIDA compliance.
It is used by a Canadian bank to filter job applications,
processes 50,000 applications per year, and uses NLP to rank
candidates by qualification match."

Result: System classified as high-impact AI (employment decisions,
significant impact on individuals). AIDA obligations triggered:
mandatory impact assessment required, bias auditing for protected
grounds (Canadian Human Rights Act), transparency notice to
candidates, record-keeping for 5 years. EU AI Act crosswalk
flags Annex III high-risk (employment, worker management).
```

## Pricing

| Tier | Price | What you get |
|------|-------|-------------|
| **Free** | £0 | 10 calls/day — AI classification + compliance check |
| **Pro** | £199/mo | Unlimited + HMAC-signed attestations + verify URLs |
| **Enterprise** | £1,499/mo | Multi-tenant + co-branded reports + webhooks |

[Subscribe to Pro](https://buy.stripe.com/14A4gB3K4eUWgYR56o8k836) · [Enterprise](https://buy.stripe.com/4gM9AV80kaEG0ZT42k8k837)

## Attestation API

Every Pro/Enterprise audit produces a cryptographically signed certificate:

```
POST https://meok-attestation-api.vercel.app/sign
GET  https://meok-attestation-api.vercel.app/verify/{cert_id}
```

Zero-dep verifier: `pip install meok-attestation-verify`

## Links

- Website: [meok.ai](https://meok.ai)
- All MCP servers: [meok.ai/labs/mcp/servers](https://meok.ai/labs/mcp/servers)
- Enterprise support: nicholas@csoai.org

## License

MIT
<!-- mcp-name: io.github.CSOAI-ORG/canada-aida-ai-mcp -->
