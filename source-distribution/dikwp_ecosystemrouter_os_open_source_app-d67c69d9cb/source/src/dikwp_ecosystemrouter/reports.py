import csv
import json
from pathlib import Path
from typing import Any, Dict
from .models import EcosystemReport


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def result_to_dict(r):
    return {
        "name": r.name,
        "score": r.score,
        "level": r.level,
        "reasons": r.reasons,
        "risks": r.risks,
        "recommendations": r.recommendations,
    }


def report_to_dict(report: EcosystemReport) -> Dict[str, Any]:
    return {
        "system": "DIKWP EcosystemRouter OS",
        "version": "0.1.0",
        "portfolio_score": report.portfolio_score,
        "moat_score": report.moat_score,
        "partner_score": report.partner_score,
        "copycat_risk_score": report.copycat_risk_score,
        "official_registry_ready_count": report.official_registry_ready_count,
        "recommended_strategy": report.recommended_strategy,
        "project_scores": [result_to_dict(r) for r in report.project_scores],
        "partner_result": result_to_dict(report.partner_result),
        "copycat_result": result_to_dict(report.copycat_result),
        "commercial_routes": report.commercial_routes,
        "boundary": "This is an ecosystem routing and certification scaffold, not a legal guarantee or official regulatory approval."
    }


def write_scorecard_csv(path: Path, report: EcosystemReport) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["type", "name", "score", "level", "risk_count", "recommendation_count"])
        for r in report.project_scores:
            w.writerow(["project", r.name, r.score, r.level, len(r.risks), len(r.recommendations)])
        w.writerow(["partner", report.partner_result.name, report.partner_result.score, report.partner_result.level, len(report.partner_result.risks), len(report.partner_result.recommendations)])
        w.writerow(["copycat", report.copycat_result.name, report.copycat_result.score, report.copycat_result.level, len(report.copycat_result.risks), len(report.copycat_result.recommendations)])


def write_registry_seed(path: Path, report: EcosystemReport) -> None:
    seed = {
        "registry": "DIKWP Official Ecosystem Registry Seed",
        "version": "0.1.0",
        "projects": [
            {
                "project_name": r.name,
                "trust_level": r.level,
                "trust_score": r.score,
                "registry_status": "candidate" if r.score >= 0.68 else "repair_required"
            } for r in report.project_scores
        ],
        "partner_candidate": {
            "name": report.partner_result.name,
            "level": report.partner_result.level,
            "score": report.partner_result.score
        },
        "copycat_watch": {
            "name": report.copycat_result.name,
            "level": report.copycat_result.level,
            "risk_score": report.copycat_result.score
        }
    }
    write_json(path, seed)


def write_markdown_assets(out: Path, report: EcosystemReport) -> None:
    copycat = out / "copycat" / "copycat_response_playbook.md"
    copycat.parent.mkdir(parents=True, exist_ok=True)
    copycat.write_text(f"""# Copycat Response Playbook

## Risk level

`{report.copycat_result.level}` with score `{report.copycat_result.score}`.

## Recommended non-litigation sequence

1. Preserve evidence: screenshots, repository commit hashes, release dates, README text, badges, citations and marketing pages.
2. Compare attribution: whether Yucong Duan / DIKWP is named, whether CITATION.cff exists, whether NOTICE is preserved.
3. Check false certification: whether the project claims official DIKWP status without registry entry.
4. Send partner outreach before escalation: invite registration, citation correction and badge validation.
5. Publish a public registry clarification if the project continues to use DIKWP terms without attribution.
6. Seek professional legal review only if reputational or commercial harm is material.

## Boundary

This playbook is an evidence and communication workflow, not legal advice.
""", encoding="utf-8")

    commercial = out / "commercial_package_catalog.md"
    commercial.write_text("""# Commercial Package Catalog

## 1. Registry Starter
- Official project registry entry
- Trust scorecard
- Citation pack
- Badge review

## 2. Partner Onboarding
- Partner review
- Training session
- Attribution cleanup
- Certification path

## 3. Enterprise Trust Audit
- DIKWP project audit
- Evidence ledger
- Governance boundary
- Copycat and market positioning analysis

## 4. China Market AICAP Track
- AICAP-CN mapping
- AI+manufacturing adapter readiness
- Procurement checklist
- CommandProposal governance playbook

## 5. Training and Certification
- DIKWP Trust Steward
- DIKWP Agent Governance Steward
- DIKWP AICAP Gateway Steward
- DIKWP AnswerGraph / ProofLedger / MemoryLedger specialty tracks
""", encoding="utf-8")

    training = out / "training_certification_catalog.md"
    training.write_text("""# Training and Certification Catalog

## DIKWP Trust Steward
Audience: open-source maintainers, AI governance teams, consulting partners.

## DIKWP Ecosystem Partner
Audience: enterprises or service firms that want to build DIKWP-based solutions while preserving attribution and official registry alignment.

## DIKWP AICAP Integration Steward
Audience: China market AI+manufacturing, industrial agent, trusted hardware, edge gateway and audit platform teams.

## Renewal
Every certificate should expire and require evidence of maintained attribution, updated citation and boundary discipline.
""", encoding="utf-8")

    partner = out / "partner_onboarding_checklist.md"
    partner.write_text("""# Partner Onboarding Checklist

- [ ] Legal entity and contact verified
- [ ] DIKWP attribution accepted
- [ ] CITATION.cff or citation route accepted
- [ ] Official registry route accepted
- [ ] False certification claims removed
- [ ] Revenue-sharing or paid support path clarified
- [ ] Commercial package selected
- [ ] Human review completed
- [ ] Badge issued only after registry validation
""", encoding="utf-8")
