import argparse
import json
from pathlib import Path
from .evaluator import build_ecosystem_report
from .reports import report_to_dict, write_json, write_scorecard_csv, write_registry_seed, write_markdown_assets
from .static_audit import audit_path


def read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_evaluate(args):
    manifest = read_json(args.manifest)
    partner = read_json(args.partner)
    copycat = read_json(args.copycat)
    policy = read_json(args.policy)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report = build_ecosystem_report(manifest, partner, copycat, policy)
    write_json(out / "ecosystem_strategy_report.json", report_to_dict(report))
    write_scorecard_csv(out / "moat_scorecard.csv", report)
    write_registry_seed(out / "official_registry_seed.json", report)
    write_json(out / "partner_routing_decision.json", {"partner": report_to_dict(report)["partner_result"]})
    write_json(out / "copycat_risk_report.json", {"copycat": report_to_dict(report)["copycat_result"]})
    write_markdown_assets(out, report)
    print(json.dumps({
        "portfolio_score": report.portfolio_score,
        "moat_score": report.moat_score,
        "partner_decision": report.partner_result.level,
        "copycat_risk": report.copycat_result.level,
        "strategy": report.recommended_strategy
    }, ensure_ascii=False, indent=2))


def cmd_static_audit(args):
    result = audit_path(args.path)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_json(out, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="dikwp-ecosystemrouter")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("evaluate")
    p.add_argument("manifest")
    p.add_argument("--partner", required=True)
    p.add_argument("--copycat", required=True)
    p.add_argument("--policy", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_evaluate)

    s = sub.add_parser("static-audit")
    s.add_argument("path")
    s.add_argument("--out", required=True)
    s.set_defaults(func=cmd_static_audit)

    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
