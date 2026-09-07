import json
from pathlib import Path
from dikwp_ecosystemrouter.evaluator import build_ecosystem_report
from dikwp_ecosystemrouter.static_audit import audit_path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_ecosystem_report_scores():
    report = build_ecosystem_report(
        load("examples/sample_ecosystem_manifest.json"),
        load("examples/sample_partner_application.json"),
        load("examples/sample_copycat_application.json"),
        load("configs/default_policy.json"),
    )
    assert report.moat_score > 0.6
    assert report.partner_result.level in {"accept_as_registered_partner_candidate", "human_review_required"}
    assert report.copycat_result.level == "high_copycat_risk"


def test_project_scores_exist():
    report = build_ecosystem_report(
        load("examples/sample_ecosystem_manifest.json"),
        load("examples/sample_partner_application.json"),
        load("examples/sample_copycat_application.json"),
        load("configs/default_policy.json"),
    )
    assert len(report.project_scores) >= 5
    assert all(0 <= p.score <= 1 for p in report.project_scores)


def test_static_audit_passes():
    result = audit_path(str(ROOT / "src"))
    assert result["pass"] is True
