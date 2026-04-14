#!/usr/bin/env python3
"""
Canada AIDA (Artificial Intelligence and Data Act) Compliance MCP Server
=========================================================================
By MEOK AI Labs | https://meok.ai

Compliance assessment for Canada's Artificial Intelligence and Data Act (AIDA),
Part 3 of Bill C-27 (Digital Charter Implementation Act, 2022). Covers AI system
classification, impact assessment, compliance checking, EU AI Act crosswalks,
and documentation generation.

Reference: Bill C-27 Part 3 — Artificial Intelligence and Data Act
           Innovation, Science and Economic Development Canada guidance
           Companion: Consumer Privacy Protection Act (CPPA)

Install: pip install mcp
Run:     python server.py
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Optional

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
FREE_DAILY_LIMIT = 10
_usage: dict[str, list[datetime]] = defaultdict(list)


def _check_rate_limit(caller: str = "anonymous", tier: str = "free") -> Optional[str]:
    if tier == "pro":
        return None
    now = datetime.now()
    cutoff = now - timedelta(days=1)
    _usage[caller] = [t for t in _usage[caller] if t > cutoff]
    if len(_usage[caller]) >= FREE_DAILY_LIMIT:
        return (
            f"Free tier limit reached ({FREE_DAILY_LIMIT}/day). "
            "Upgrade to MEOK AI Labs Pro for unlimited: https://meok.ai/mcp/canada-aida-ai/pro"
        )
    _usage[caller].append(now)
    return None


# ---------------------------------------------------------------------------
# FastMCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "canada-aida-ai",
    instructions=(
        "Canada AIDA (Artificial Intelligence and Data Act) compliance server. "
        "Classify AI systems as high-impact or general under AIDA, perform impact "
        "assessments, check compliance obligations, crosswalk to EU AI Act, and "
        "generate AIDA compliance documentation. By MEOK AI Labs."
    ),
)

# ---------------------------------------------------------------------------
# AIDA Knowledge Base — Bill C-27 Part 3
# ---------------------------------------------------------------------------

AIDA_FRAMEWORK = {
    "overview": {
        "full_name": "Artificial Intelligence and Data Act (AIDA)",
        "legislation": "Bill C-27, Part 3 — Digital Charter Implementation Act, 2022",
        "status": "Proposed legislation — Parliament of Canada",
        "scope": "Regulates AI systems in international and interprovincial trade and commerce in Canada",
        "key_terms": {
            "artificial_intelligence_system": "A technological system that, using a model, processes data related to human activities through the use of a genetic algorithm, a neural network, machine learning or another technique in order to generate content or make decisions, recommendations or predictions.",
            "high_impact_system": "An AI system that meets criteria prescribed by regulation, considering potential impacts on health, safety, human rights, and other factors.",
            "responsible_person": "The person who, in the course of international or interprovincial trade and commerce, designs, develops, makes available for use, or manages the operation of an AI system.",
        },
    },
    "obligations": {
        "general": {
            "section_5": {
                "title": "Anonymized data — measures",
                "description": "A person who, in the course of international or interprovincial trade and commerce, carries out any regulated activity in relation to an AI system that processes or makes available for use anonymized data shall establish measures with respect to the manner in which data is anonymized and the use or management of anonymized data.",
            },
            "section_6": {
                "title": "General duty — responsible persons",
                "description": "A person who is responsible for an AI system shall assess whether it is a high-impact system.",
            },
            "section_7": {
                "title": "Measures — high-impact systems",
                "description": "A person responsible for a high-impact system shall establish measures to identify, assess and mitigate risks of harm or biased output.",
            },
            "section_8": {
                "title": "Monitoring obligations",
                "description": "A person responsible for a high-impact system shall establish measures to monitor compliance and the mitigation measures.",
            },
            "section_9": {
                "title": "Records keeping",
                "description": "A responsible person shall keep records describing the measures established under sections 5 to 8.",
            },
            "section_10": {
                "title": "Transparency — high-impact systems",
                "description": "A person who makes available for use a high-impact system shall publish on a publicly available website a plain-language description of the system that explains: (a) how the system is intended to be used; (b) the types of content it is intended to generate or decisions, recommendations or predictions it is intended to make; (c) the mitigation measures established; and (d) any other prescribed information.",
            },
            "section_11": {
                "title": "Notification to affected persons",
                "description": "A person who manages the operation of a high-impact system shall notify any person if the use of the system resulted or is likely to result in material harm to the person.",
            },
            "section_12": {
                "title": "Notification to Minister",
                "description": "If a responsible person has reason to believe that the use of the high-impact system may result in material harm, the person shall as soon as feasible notify the Minister and take reasonable measures to mitigate the harm.",
            },
        },
        "prohibitions": {
            "section_38": {
                "title": "Possession or use for harm",
                "description": "It is prohibited to possess or use personal information obtained by an AI system, knowing that or being reckless as to whether the information was obtained through the commission of an offence.",
            },
            "section_39": {
                "title": "Making available for harm",
                "description": "A person must not make available for use an AI system if they know or ought reasonably to know that the system is likely to cause serious physical or psychological harm to an individual, or substantial damage to property.",
            },
        },
    },
    "enforcement": {
        "ai_data_commissioner": "The Minister may designate an individual as the Artificial Intelligence and Data Commissioner to support administration and enforcement of AIDA.",
        "penalties": {
            "summary_conviction": "Fine up to $10,000,000 or 3% of gross global revenue, whichever is greater",
            "indictable_offence": "Fine up to $25,000,000 or 5% of gross global revenue, whichever is greater, and/or imprisonment up to 5 years for individuals",
        },
        "compliance_orders": "The Minister may order a responsible person to cease using or making available a high-impact system, provide records, or take corrective measures.",
    },
}

# ---------------------------------------------------------------------------
# High-Impact Classification Criteria
# ---------------------------------------------------------------------------

HIGH_IMPACT_CRITERIA = {
    "health_safety": {
        "title": "Health and safety impact",
        "description": "AI system that could adversely affect the health or safety of an individual",
        "examples": [
            "Medical diagnosis or treatment recommendations",
            "Autonomous vehicle control systems",
            "Industrial safety monitoring",
            "Drug discovery and clinical trial AI",
            "Mental health assessment or intervention AI",
        ],
        "weight": 5,
    },
    "human_rights": {
        "title": "Impact on human rights",
        "description": "AI system that could adversely affect an individual's human rights",
        "examples": [
            "Facial recognition for identification",
            "Criminal risk assessment or sentencing",
            "Immigration or asylum decision support",
            "Social scoring or social credit systems",
            "Content moderation affecting freedom of expression",
        ],
        "weight": 5,
    },
    "economic_impact": {
        "title": "Economic impact on individuals",
        "description": "AI system that could cause significant economic consequences to individuals",
        "examples": [
            "Credit scoring and lending decisions",
            "Employment screening and hiring",
            "Insurance underwriting",
            "Benefits eligibility determination",
            "Salary and compensation algorithms",
        ],
        "weight": 4,
    },
    "vulnerable_populations": {
        "title": "Impact on vulnerable populations",
        "description": "AI system deployed in contexts involving vulnerable populations (children, elderly, disabled, Indigenous)",
        "examples": [
            "Child welfare decision support",
            "Educational AI for children",
            "Elder care monitoring",
            "Disability assessment AI",
            "Indigenous community impact assessment",
        ],
        "weight": 5,
    },
    "scale_of_impact": {
        "title": "Scale and scope of impact",
        "description": "AI system with broad reach or systemic effects across populations",
        "examples": [
            "Public infrastructure management",
            "Energy grid optimization",
            "Financial market algorithms",
            "National security applications",
            "Large-scale content recommendation",
        ],
        "weight": 3,
    },
    "biased_output_risk": {
        "title": "Risk of biased output",
        "description": "AI system with elevated risk of producing discriminatory outcomes",
        "examples": [
            "Predictive policing",
            "Resume screening",
            "Targeted advertising (housing, employment, credit)",
            "Facial analysis (emotion, age, gender)",
            "Language processing that may disadvantage non-English speakers",
        ],
        "weight": 4,
    },
}

# ---------------------------------------------------------------------------
# AIDA to EU AI Act Crosswalk
# ---------------------------------------------------------------------------

AIDA_EU_AI_ACT_CROSSWALK = {
    "classification": {
        "aida": "Section 6 — High-impact system classification",
        "eu_ai_act": "Article 6, Annex III — High-risk AI classification",
        "alignment": "strong",
        "note": "Both use risk-based classification. AIDA delegates criteria to regulation while EU AI Act specifies in Annex III. Canada's approach is broader and more flexible. EU AI Act also defines 'unacceptable risk' (prohibited) category that AIDA lacks.",
    },
    "risk_mitigation": {
        "aida": "Section 7 — Measures for high-impact systems",
        "eu_ai_act": "Article 9 — Risk management system",
        "alignment": "strong",
        "note": "Both require identification, assessment, and mitigation of risks. EU AI Act is more prescriptive with specific risk management system requirements. AIDA is principles-based.",
    },
    "monitoring": {
        "aida": "Section 8 — Monitoring obligations",
        "eu_ai_act": "Article 9(2)(b) — Post-market monitoring, Article 72",
        "alignment": "strong",
        "note": "Both require ongoing monitoring of high-risk AI. EU AI Act specifies post-market monitoring plans. AIDA requires monitoring of compliance and mitigation measures.",
    },
    "recordkeeping": {
        "aida": "Section 9 — Records keeping",
        "eu_ai_act": "Article 12 — Record-keeping (logging)",
        "alignment": "strong",
        "note": "Both require records/logs. EU AI Act is more specific about automatic logging capabilities and traceability requirements.",
    },
    "transparency": {
        "aida": "Section 10 — Transparency (public description)",
        "eu_ai_act": "Article 13 — Transparency, Article 52 — Transparency for certain AI",
        "alignment": "strong",
        "note": "Both require transparency for high-risk AI. AIDA requires public website description. EU AI Act requires technical documentation and instructions for use to deployers.",
    },
    "notification_harm": {
        "aida": "Section 11 — Notification to affected persons",
        "eu_ai_act": "Article 62 — Reporting of serious incidents",
        "alignment": "partial",
        "note": "AIDA focuses on notification to affected individuals. EU AI Act requires reporting to market surveillance authorities. Different notification recipients and triggers.",
    },
    "notification_minister": {
        "aida": "Section 12 — Notification to Minister",
        "eu_ai_act": "Article 62 — Reporting of serious incidents to authorities",
        "alignment": "strong",
        "note": "Both require government notification. AIDA notifies the Minister; EU AI Act notifies market surveillance authorities.",
    },
    "prohibition_harm": {
        "aida": "Section 39 — Making available AI likely to cause serious harm",
        "eu_ai_act": "Article 5 — Prohibited AI practices",
        "alignment": "partial",
        "note": "AIDA has a general prohibition on AI likely to cause serious harm. EU AI Act has specific enumerated prohibited practices (social scoring, real-time biometric surveillance, etc.). EU AI Act is more specific; AIDA is broader but less defined.",
    },
    "enforcement_penalties": {
        "aida": "Penalties up to $25M or 5% global revenue",
        "eu_ai_act": "Article 99 — Fines up to EUR 35M or 7% global revenue",
        "alignment": "partial",
        "note": "Both impose significant penalties. EU AI Act fines are higher (7% vs 5%). AIDA includes criminal penalties (imprisonment) that EU AI Act does not.",
    },
    "anonymized_data": {
        "aida": "Section 5 — Anonymized data measures",
        "eu_ai_act": "No direct equivalent",
        "alignment": "gap",
        "note": "AIDA uniquely addresses anonymized data governance. EU AI Act defers data handling to GDPR. This is a distinctive Canadian provision.",
    },
}


# ---------------------------------------------------------------------------
# TOOL 1: Classify AI System
# ---------------------------------------------------------------------------
@mcp.tool()
def classify_ai_system(
    system_description: str,
    system_purpose: str,
    target_users: list[str],
    data_types: list[str],
    deployment_context: str = "commercial",
    interprovincial_trade: bool = True,
    caller: str = "anonymous",
    tier: str = "free",
) -> str:
    """Classify an AI system under AIDA as high-impact or general-purpose.
    Evaluates against high-impact criteria including health/safety, human rights,
    economic impact, vulnerable populations, and bias risk.

    Args:
        system_description: Description of the AI system
        system_purpose: Primary purpose of the AI system
        target_users: Who uses or is affected by the system (e.g. ["patients", "employees", "children"])
        data_types: Types of data the system processes (e.g. ["personal", "health", "biometric"])
        deployment_context: Context of deployment: "commercial", "government", "healthcare", "finance", "education"
        interprovincial_trade: Whether the system operates in interprovincial or international trade (AIDA scope)
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    if err := _check_rate_limit(caller, tier):
        return json.dumps({"error": err})

    if not interprovincial_trade:
        return json.dumps({
            "classification": "OUT_OF_SCOPE",
            "note": "AIDA applies only to AI systems in international and interprovincial trade and commerce. Provincial legislation may apply.",
        })

    desc_lower = system_description.lower() + " " + system_purpose.lower()
    users_lower = " ".join(target_users).lower()
    data_lower = " ".join(data_types).lower()

    impact_scores = {}
    total_score = 0
    triggered_criteria = []

    for criterion_key, criterion in HIGH_IMPACT_CRITERIA.items():
        score = 0
        examples_lower = " ".join(criterion["examples"]).lower()

        # Check description match
        keywords = {
            "health_safety": ["health", "medical", "safety", "clinical", "diagnosis", "treatment", "autonomous"],
            "human_rights": ["facial recognition", "criminal", "immigration", "identification", "biometric", "scoring"],
            "economic_impact": ["credit", "lending", "hiring", "employment", "insurance", "benefits", "salary"],
            "vulnerable_populations": ["child", "children", "elderly", "disabled", "indigenous", "minor"],
            "scale_of_impact": ["infrastructure", "grid", "financial market", "national", "large-scale"],
            "biased_output_risk": ["screening", "prediction", "policing", "advertising", "targeting", "profiling"],
        }

        kws = keywords.get(criterion_key, [])
        matches = sum(1 for kw in kws if kw in desc_lower or kw in users_lower or kw in data_lower)

        if matches >= 2:
            score = criterion["weight"]
        elif matches >= 1:
            score = criterion["weight"] // 2

        # Context boost
        context_boost = {
            "healthcare": ["health_safety"],
            "finance": ["economic_impact"],
            "government": ["human_rights", "scale_of_impact"],
            "education": ["vulnerable_populations"],
        }
        if criterion_key in context_boost.get(deployment_context, []):
            score = max(score, criterion["weight"] // 2)

        if score > 0:
            triggered_criteria.append({
                "criterion": criterion_key,
                "title": criterion["title"],
                "score": score,
                "max_score": criterion["weight"],
            })

        impact_scores[criterion_key] = score
        total_score += score

    # Classification
    if total_score >= 10:
        classification = "HIGH_IMPACT"
        confidence = "high"
    elif total_score >= 5:
        classification = "HIGH_IMPACT"
        confidence = "medium"
    elif total_score >= 3:
        classification = "LIKELY_HIGH_IMPACT"
        confidence = "low"
    else:
        classification = "GENERAL"
        confidence = "high"

    is_high_impact = classification in ("HIGH_IMPACT", "LIKELY_HIGH_IMPACT")

    result = {
        "classification_type": "AIDA AI System Classification",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system": {
            "description": system_description,
            "purpose": system_purpose,
            "target_users": target_users,
            "data_types": data_types,
            "deployment_context": deployment_context,
        },
        "classification": {
            "result": classification,
            "confidence": confidence,
            "impact_score": total_score,
            "triggered_criteria": triggered_criteria,
        },
        "obligations": {
            "section_5_anonymized_data": any(d in data_lower for d in ["anonymized", "de-identified"]),
            "section_6_assessment_required": True,
            "section_7_risk_mitigation": is_high_impact,
            "section_8_monitoring": is_high_impact,
            "section_9_recordkeeping": is_high_impact,
            "section_10_transparency": is_high_impact,
            "section_11_notification_affected": is_high_impact,
            "section_12_notification_minister": is_high_impact,
        },
        "penalties_exposure": (
            AIDA_FRAMEWORK["enforcement"]["penalties"]
            if is_high_impact
            else {"note": "General systems have fewer obligations but Section 39 (harm prohibition) still applies"}
        ),
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# TOOL 2: Impact Assessment
# ---------------------------------------------------------------------------
@mcp.tool()
def impact_assessment(
    system_name: str,
    system_description: str,
    affected_populations: list[str],
    risk_scenarios: Optional[list[str]] = None,
    mitigation_measures: Optional[list[str]] = None,
    caller: str = "anonymous",
    tier: str = "free",
) -> str:
    """Perform an AI impact assessment per AIDA requirements (Sections 7-8).
    Evaluates potential harms, biased output risks, and required mitigation
    measures for high-impact AI systems.

    Args:
        system_name: Name of the AI system
        system_description: Detailed description of the system and its function
        affected_populations: Groups of people affected by the system
        risk_scenarios: Specific risk scenarios to evaluate
        mitigation_measures: Currently implemented mitigation measures
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    if err := _check_rate_limit(caller, tier):
        return json.dumps({"error": err})

    existing_mitigations = set(m.lower() for m in (mitigation_measures or []))

    default_risks = [
        "Biased output disproportionately affecting marginalized groups",
        "Inaccurate predictions or decisions causing material harm",
        "Privacy violations through data processing",
        "Lack of transparency in automated decision-making",
        "System failure or degraded performance affecting availability",
        "Unauthorized access or adversarial manipulation",
    ]

    risks_to_assess = risk_scenarios or default_risks

    risk_register = []
    for risk in risks_to_assess:
        risk_lower = risk.lower()

        # Impact assessment
        if any(w in risk_lower for w in ["bias", "discrimination", "marginalized", "unfair"]):
            impact = "high"
            category = "biased_output"
            required_mitigations = ["Bias testing across protected groups", "Regular disparate impact analysis", "Diverse training data review", "Human oversight for high-stakes decisions"]
        elif any(w in risk_lower for w in ["harm", "safety", "health", "injury"]):
            impact = "critical"
            category = "health_safety"
            required_mitigations = ["Safety testing and validation", "Fail-safe mechanisms", "Human-in-the-loop for safety-critical decisions", "Emergency shutdown procedures"]
        elif any(w in risk_lower for w in ["privacy", "data", "personal information"]):
            impact = "high"
            category = "privacy"
            required_mitigations = ["Privacy impact assessment", "Data minimization", "Anonymization/pseudonymization", "Compliance with CPPA (Consumer Privacy Protection Act)"]
        elif any(w in risk_lower for w in ["transparency", "explainability", "opaque"]):
            impact = "medium"
            category = "transparency"
            required_mitigations = ["Plain-language system description (Section 10)", "Explainability mechanisms", "Notification procedures (Section 11)"]
        else:
            impact = "medium"
            category = "general"
            required_mitigations = ["Regular system monitoring", "Incident response procedures", "Compliance review"]

        mitigated = any(any(rm.lower() in em for em in existing_mitigations) for rm in required_mitigations[:2])

        risk_register.append({
            "risk": risk,
            "category": category,
            "impact": impact,
            "residual_impact": "low" if mitigated else impact,
            "mitigated": mitigated,
            "required_mitigations": required_mitigations,
        })

    unmitigated = [r for r in risk_register if not r["mitigated"]]

    result = {
        "assessment_type": "AIDA Impact Assessment (Sections 7-8)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system_name": system_name,
        "system_description": system_description,
        "affected_populations": affected_populations,
        "risk_assessment": risk_register,
        "summary": {
            "total_risks": len(risk_register),
            "mitigated_risks": len(risk_register) - len(unmitigated),
            "unmitigated_risks": len(unmitigated),
            "critical_risks": len([r for r in risk_register if r["impact"] == "critical"]),
            "overall_risk": "HIGH" if any(r["impact"] == "critical" for r in unmitigated) else "MEDIUM" if unmitigated else "LOW",
        },
        "aida_compliance_requirements": {
            "section_7": "Establish measures to identify, assess and mitigate risks of harm or biased output",
            "section_8": "Monitor compliance with mitigation measures on ongoing basis",
            "section_9": "Keep records describing measures established",
            "section_10": "Publish plain-language system description",
            "section_11": "Notify affected persons if material harm results",
            "section_12": "Notify Minister if material harm may result",
        },
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# TOOL 3: Compliance Check
# ---------------------------------------------------------------------------
@mcp.tool()
def compliance_check(
    system_classification: str,
    measures_in_place: list[str],
    records_maintained: bool = False,
    public_description_published: bool = False,
    monitoring_active: bool = False,
    notification_procedures: bool = False,
    caller: str = "anonymous",
    tier: str = "free",
) -> str:
    """Check compliance with AIDA obligations. Evaluates whether a responsible
    person meets all AIDA requirements for their AI system classification.

    Args:
        system_classification: Classification result: "HIGH_IMPACT" or "GENERAL"
        measures_in_place: List of compliance measures implemented
        records_maintained: Whether Section 9 records are being kept
        public_description_published: Whether Section 10 public description is published
        monitoring_active: Whether Section 8 monitoring is in place
        notification_procedures: Whether Sections 11-12 notification procedures exist
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    if err := _check_rate_limit(caller, tier):
        return json.dumps({"error": err})

    is_high = system_classification.upper() == "HIGH_IMPACT"
    measures_lower = set(m.lower() for m in measures_in_place)

    checks = [
        {
            "section": "Section 5",
            "requirement": "Anonymized data measures",
            "applicable": True,
            "status": any("anonymi" in m for m in measures_lower),
            "priority": "medium",
        },
        {
            "section": "Section 6",
            "requirement": "High-impact assessment completed",
            "applicable": True,
            "status": True,  # If they're running this check, they've assessed
            "priority": "critical",
        },
        {
            "section": "Section 7",
            "requirement": "Risk mitigation measures established",
            "applicable": is_high,
            "status": any("risk" in m or "mitigation" in m for m in measures_lower),
            "priority": "critical",
        },
        {
            "section": "Section 8",
            "requirement": "Ongoing monitoring in place",
            "applicable": is_high,
            "status": monitoring_active,
            "priority": "critical",
        },
        {
            "section": "Section 9",
            "requirement": "Records maintained",
            "applicable": is_high,
            "status": records_maintained,
            "priority": "high",
        },
        {
            "section": "Section 10",
            "requirement": "Public plain-language description published",
            "applicable": is_high,
            "status": public_description_published,
            "priority": "high",
        },
        {
            "section": "Section 11",
            "requirement": "Notification procedures for affected persons",
            "applicable": is_high,
            "status": notification_procedures,
            "priority": "high",
        },
        {
            "section": "Section 12",
            "requirement": "Notification procedures for Minister",
            "applicable": is_high,
            "status": notification_procedures,
            "priority": "high",
        },
        {
            "section": "Section 39",
            "requirement": "System not likely to cause serious harm",
            "applicable": True,
            "status": not any("serious harm" in m for m in measures_lower),
            "priority": "critical",
        },
    ]

    applicable_checks = [c for c in checks if c["applicable"]]
    passed = [c for c in applicable_checks if c["status"]]
    failed = [c for c in applicable_checks if not c["status"]]
    compliance_pct = (len(passed) / len(applicable_checks) * 100) if applicable_checks else 0

    result = {
        "compliance_type": "AIDA Compliance Check",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "system_classification": system_classification,
        "compliance_checks": applicable_checks,
        "summary": {
            "total_checks": len(applicable_checks),
            "passed": len(passed),
            "failed": len(failed),
            "compliance_percent": round(compliance_pct, 1),
            "overall_status": "COMPLIANT" if not failed else "NON-COMPLIANT",
            "critical_failures": [c["section"] + ": " + c["requirement"] for c in failed if c["priority"] == "critical"],
        },
        "penalties_risk": {
            "non_compliance_detected": bool(failed),
            "max_penalty_summary": AIDA_FRAMEWORK["enforcement"]["penalties"]["summary_conviction"] if failed else "N/A",
            "max_penalty_indictable": AIDA_FRAMEWORK["enforcement"]["penalties"]["indictable_offence"] if failed else "N/A",
        },
        "remediation": [
            {"section": c["section"], "action": f"Implement: {c['requirement']}", "priority": c["priority"]}
            for c in failed
        ],
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# TOOL 4: Crosswalk to EU AI Act
# ---------------------------------------------------------------------------
@mcp.tool()
def crosswalk_to_eu_ai_act(
    focus_area: str = "all",
    caller: str = "anonymous",
    tier: str = "free",
) -> str:
    """Map AIDA requirements to EU AI Act obligations. Essential for
    organizations operating in both Canadian and European markets, showing
    where compliance overlaps and where additional measures are needed.

    Args:
        focus_area: Focus on "all", "classification", "transparency", "enforcement", or "risk_management"
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    if err := _check_rate_limit(caller, tier):
        return json.dumps({"error": err})

    focus_filters = {
        "classification": ["classification"],
        "transparency": ["transparency", "notification_harm", "notification_minister"],
        "enforcement": ["enforcement_penalties", "prohibition_harm"],
        "risk_management": ["risk_mitigation", "monitoring", "recordkeeping"],
    }

    if focus_area in focus_filters:
        target_keys = focus_filters[focus_area]
    else:
        target_keys = list(AIDA_EU_AI_ACT_CROSSWALK.keys())

    mappings = []
    strong = 0
    partial = 0
    gap = 0

    for key in target_keys:
        if key not in AIDA_EU_AI_ACT_CROSSWALK:
            continue
        xw = AIDA_EU_AI_ACT_CROSSWALK[key]
        mappings.append({
            "mapping_id": key,
            "aida_provision": xw["aida"],
            "eu_ai_act_provision": xw["eu_ai_act"],
            "alignment": xw["alignment"],
            "analysis": xw["note"],
        })
        if xw["alignment"] == "strong":
            strong += 1
        elif xw["alignment"] == "partial":
            partial += 1
        elif xw["alignment"] == "gap":
            gap += 1

    result = {
        "crosswalk_type": "AIDA to EU AI Act Regulatory Crosswalk",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "focus_area": focus_area,
        "mappings": mappings,
        "summary": {
            "total_mappings": len(mappings),
            "strong_alignment": strong,
            "partial_alignment": partial,
            "gaps": gap,
        },
        "key_differences": [
            "EU AI Act has explicit prohibited practices list; AIDA uses general harm prohibition",
            "EU AI Act specifies high-risk categories in Annex III; AIDA delegates to regulation",
            "AIDA includes criminal penalties (imprisonment); EU AI Act has only fines",
            "AIDA uniquely addresses anonymized data governance (Section 5)",
            "EU AI Act has broader territorial scope and more detailed technical requirements",
            "AIDA is principles-based; EU AI Act is more prescriptive",
        ],
        "dual_compliance_recommendation": (
            "Organizations operating in both Canada and the EU should use EU AI Act compliance "
            "as the baseline (more prescriptive) and layer AIDA-specific requirements on top: "
            "anonymized data measures (Section 5), Canadian notification to Minister (Section 12), "
            "and plain-language public description (Section 10). EU AI Act compliance will satisfy "
            "most AIDA requirements but not all."
        ),
    }

    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# TOOL 5: Generate Documentation
# ---------------------------------------------------------------------------
@mcp.tool()
def generate_documentation(
    system_name: str,
    system_description: str,
    classification: str,
    responsible_person: str,
    document_type: str = "public_description",
    caller: str = "anonymous",
    tier: str = "free",
) -> str:
    """Generate AIDA compliance documentation including public system
    descriptions (Section 10), compliance records (Section 9), and
    notification templates (Sections 11-12).

    Args:
        system_name: Name of the AI system
        system_description: Description of the AI system
        classification: AIDA classification: "HIGH_IMPACT" or "GENERAL"
        responsible_person: Name/org of the responsible person under AIDA
        document_type: Type of document: "public_description", "compliance_record", "notification_affected", "notification_minister"
        caller: Caller identifier for rate limiting
        tier: Access tier (free/pro)
    """
    if err := _check_rate_limit(caller, tier):
        return json.dumps({"error": err})

    timestamp = datetime.now(timezone.utc).isoformat()

    if document_type == "public_description":
        doc = {
            "document_type": "AIDA Section 10 — Public Description of High-Impact AI System",
            "timestamp": timestamp,
            "responsible_person": responsible_person,
            "system_name": system_name,
            "section_a_intended_use": {
                "description": system_description,
                "instruction": "[Describe in plain language how the system is intended to be used, including the context and environment of deployment]",
            },
            "section_b_content_and_decisions": {
                "instruction": "[Describe the types of content the system generates OR the types of decisions, recommendations, or predictions it makes]",
            },
            "section_c_mitigation_measures": {
                "instruction": "[Describe the measures established to identify, assess, and mitigate risks of harm or biased output, per Section 7]",
                "required_elements": [
                    "Risk identification methodology",
                    "Bias testing procedures and results summary",
                    "Human oversight mechanisms",
                    "Monitoring and update procedures",
                    "Complaint and redress mechanisms",
                ],
            },
            "section_d_additional_information": {
                "instruction": "[Include any other information prescribed by regulation]",
                "suggested_elements": [
                    "Data types processed",
                    "Training data description",
                    "Performance metrics and limitations",
                    "Contact information for inquiries",
                    "Date of last update",
                ],
            },
            "publication_requirements": {
                "where": "Publicly available website",
                "language": "Plain language accessible to affected persons",
                "updates": "Must be updated when system changes materially",
            },
        }
    elif document_type == "compliance_record":
        doc = {
            "document_type": "AIDA Section 9 — Compliance Records",
            "timestamp": timestamp,
            "responsible_person": responsible_person,
            "system_name": system_name,
            "classification": classification,
            "record_sections": {
                "section_5_records": {
                    "title": "Anonymized Data Measures",
                    "content": "[Document anonymization methods, usage rules, and management procedures]",
                },
                "section_6_records": {
                    "title": "High-Impact Assessment",
                    "content": "[Document the assessment methodology and conclusion for high-impact classification]",
                },
                "section_7_records": {
                    "title": "Risk Mitigation Measures",
                    "content": "[Document all measures to identify, assess, and mitigate risks of harm or biased output]",
                    "required_elements": [
                        "Risk register with identified risks",
                        "Mitigation measures for each risk",
                        "Bias testing methodology and results",
                        "Human oversight procedures",
                    ],
                },
                "section_8_records": {
                    "title": "Monitoring Records",
                    "content": "[Document ongoing monitoring activities and results]",
                    "required_elements": [
                        "Monitoring frequency and methodology",
                        "Monitoring results and trends",
                        "Corrective actions taken",
                        "Compliance status updates",
                    ],
                },
            },
            "retention": "Records must be maintained for the operational life of the system and as prescribed by regulation",
        }
    elif document_type == "notification_affected":
        doc = {
            "document_type": "AIDA Section 11 — Notification to Affected Persons Template",
            "timestamp": timestamp,
            "responsible_person": responsible_person,
            "system_name": system_name,
            "template": {
                "subject": f"Notice: Potential Impact from AI System — {system_name}",
                "body_elements": [
                    "1. Description of the AI system and its use",
                    "2. Nature of the material harm that resulted or is likely to result",
                    "3. When the harm occurred or was identified",
                    "4. What information or decisions were affected",
                    "5. Measures being taken to mitigate the harm",
                    "6. Contact information for questions or complaints",
                    "7. Information about available recourse or remediation",
                ],
                "timing": "As soon as feasible after becoming aware of the harm",
                "method": "Direct notification to affected individuals by appropriate means",
            },
        }
    elif document_type == "notification_minister":
        doc = {
            "document_type": "AIDA Section 12 — Notification to Minister Template",
            "timestamp": timestamp,
            "responsible_person": responsible_person,
            "system_name": system_name,
            "template": {
                "recipient": "Minister of Innovation, Science and Economic Development Canada",
                "body_elements": [
                    "1. Identity of the responsible person and contact information",
                    "2. Description of the high-impact AI system",
                    "3. Nature of the material harm that may result",
                    "4. Circumstances giving rise to the belief of potential harm",
                    "5. Number of persons potentially affected",
                    "6. Measures being taken to mitigate the risk",
                    "7. Timeline for corrective action",
                ],
                "timing": "As soon as feasible after forming reasonable belief of potential material harm",
                "note": "The Minister may issue compliance orders including cessation of system use",
            },
        }
    else:
        return json.dumps({"error": f"Unknown document_type: {document_type}. Valid: public_description, compliance_record, notification_affected, notification_minister"})

    return json.dumps(doc, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
