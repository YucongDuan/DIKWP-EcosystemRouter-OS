from typing import Any, Dict, List, Tuple
from .models import ProjectRecord, PartnerApplication, EcosystemPolicy, ScoreResult, EcosystemReport
from .text_utils import clamp, contains_any

DIKWP_LAYER_SET = {"D", "I", "K", "W", "P", "R", "Data", "Information", "Knowledge", "Wisdom", "Purpose", "Reliability"}
COPYCAT_TERMS = ["no attribution", "remove attribution", "rebrand", "hide origin", "official without approval", "exclusive owner", "guaranteed certification"]
RISKY_CLAIM_TERMS = ["official certification", "guaranteed", "exclusive", "government approved", "no audit needed", "replace legal review"]


def load_project_records(raw: Dict[str, Any]) -> List[ProjectRecord]:
    records = []
    for item in raw.get("projects", []):
        records.append(ProjectRecord(**item))
    return records


def load_partner(raw: Dict[str, Any]) -> PartnerApplication:
    return PartnerApplication(**raw)


def load_policy(raw: Dict[str, Any]) -> EcosystemPolicy:
    return EcosystemPolicy(**raw)


def score_project(project: ProjectRecord) -> ScoreResult:
    reasons: List[str] = []
    risks: List[str] = []
    recs: List[str] = []

    score = 0.0
    if any("Duan" in a or "DIKWP" in a for a in project.attribution):
        score += 0.20
        reasons.append("Explicit Yucong Duan / DIKWP attribution present.")
    else:
        risks.append("Missing explicit DIKWP attribution.")
        recs.append("Add NOTICE and CITATION.cff with Yucong Duan / DIKWP attribution.")

    layers = set(project.dikwp_layers)
    layer_score = len(layers.intersection(DIKWP_LAYER_SET)) / 6.0
    score += 0.24 * clamp(layer_score)
    if layer_score >= 0.8:
        reasons.append("Strong DIKWP layer coverage.")
    else:
        risks.append("DIKWP layer coverage is incomplete or superficial.")
        recs.append("Map product functions to D/I/K/W/P/R explicitly.")

    if project.tests:
        score += 0.12
        reasons.append("Tests are declared.")
    else:
        risks.append("No tests declared.")

    if project.demo_outputs:
        score += 0.12
        reasons.append("Demo outputs are declared.")
    else:
        recs.append("Add demo outputs and QA report.")

    if project.official_assets:
        score += 0.14
        reasons.append("Official ecosystem assets are present.")
    else:
        recs.append("Add registry entry, trust badge, commercial route card, and citation pack.")

    if project.commercial_routes:
        score += 0.10
        reasons.append("Commercial routes are visible.")
    else:
        risks.append("No benefit-capture route declared.")

    if project.copycat_risks:
        risk_penalty = min(0.12, len(project.copycat_risks) * 0.03)
        score -= risk_penalty
        risks.extend(project.copycat_risks)
        recs.append("Mitigate copycat risks through registry, badge, partner program, and evidence ledger.")

    score = clamp(score)
    level = "registry_ready" if score >= 0.75 else "needs_repair" if score >= 0.45 else "not_ready"
    return ScoreResult(project.name, round(score, 4), level, reasons, risks, recs)


def score_partner(app: PartnerApplication, policy: EcosystemPolicy) -> ScoreResult:
    reasons: List[str] = []
    risks: List[str] = []
    recs: List[str] = []
    score = 0.0

    if app.attribution_commitment:
        score += 0.18
        reasons.append("Partner commits to DIKWP attribution.")
    else:
        risks.append("No attribution commitment.")

    if app.citation_commitment:
        score += 0.14
        reasons.append("Partner commits to citation discipline.")
    else:
        risks.append("No citation commitment.")

    if app.official_registry_commitment:
        score += 0.18
        reasons.append("Partner agrees to official registry route.")
    else:
        risks.append("Partner may bypass official registry.")

    if app.certification_interest:
        score += 0.12
        reasons.append("Partner is interested in certification.")

    if app.revenue_share_interest:
        score += 0.12
        reasons.append("Partner is open to revenue-sharing or commercial cooperation.")

    capability_score = min(0.18, len(app.partner_capabilities) * 0.03)
    score += capability_score
    if capability_score > 0:
        reasons.append("Partner declares implementation or market capabilities.")

    text = " ".join([app.proposed_use] + app.risky_claims)
    risky = [term for term in RISKY_CLAIM_TERMS if term in text.lower()]
    if risky or app.risky_claims:
        penalty = min(0.30, 0.08 * len(risky) + 0.04 * len(app.risky_claims))
        score -= penalty
        risks.extend(app.risky_claims or risky)
        recs.append("Remove claims of official approval, guaranteed outcomes, or certification without registry verification.")

    if app.missing_items:
        penalty = min(0.20, 0.04 * len(app.missing_items))
        score -= penalty
        risks.extend([f"Missing: {x}" for x in app.missing_items])

    score = clamp(score)
    if score >= policy.min_partner_score:
        level = "accept_as_registered_partner_candidate"
        recs.append("Route to official partner onboarding and training package.")
    elif score >= 0.45:
        level = "human_review_required"
        recs.append("Request attribution, registry, certification, and legal/marketing cleanup before approval.")
    else:
        level = "reject_or_watchlist"
        recs.append("Do not grant official badge; monitor copycat or misattribution risk.")
    return ScoreResult(app.applicant_name, round(score, 4), level, reasons, risks, recs)


def score_copycat(app: PartnerApplication, policy: EcosystemPolicy) -> ScoreResult:
    reasons: List[str] = []
    risks: List[str] = []
    recs: List[str] = []
    score = 0.0
    text = " ".join([app.proposed_use] + app.risky_claims + app.missing_items)

    if not app.attribution_commitment:
        score += 0.25
        risks.append("Missing attribution commitment.")
    if not app.citation_commitment:
        score += 0.15
        risks.append("Missing citation commitment.")
    if not app.official_registry_commitment:
        score += 0.20
        risks.append("No official registry route.")
    if contains_any(text, COPYCAT_TERMS + RISKY_CLAIM_TERMS):
        score += 0.25
        risks.append("Text contains copycat or false-certification indicators.")
    if app.revenue_share_interest is False:
        score += 0.05
    if app.certification_interest is False:
        score += 0.05
    if app.missing_items:
        score += min(0.10, 0.02 * len(app.missing_items))

    score = clamp(score)
    level = "high_copycat_risk" if score >= policy.copycat_high_risk_threshold else "medium_copycat_risk" if score >= 0.35 else "low_copycat_risk"
    reasons.append("Copycat score measures attribution, registry bypass, false certification and commercial appropriation risk.")
    recs.extend([
        "Do not grant badge without verified attribution and registry entry.",
        "Generate public clarification and partner outreach pack if DIKWP terminology is used without citation.",
        "Prefer ecosystem routing, certification and training benefits over exposing core strategic assets."
    ])
    return ScoreResult(app.applicant_name, round(score, 4), level, reasons, risks, recs)


def build_ecosystem_report(raw_manifest: Dict[str, Any], partner_raw: Dict[str, Any], copycat_raw: Dict[str, Any], policy_raw: Dict[str, Any]) -> EcosystemReport:
    policy = load_policy(policy_raw)
    projects = load_project_records(raw_manifest)
    project_scores = [score_project(p) for p in projects]
    portfolio_score = sum(p.score for p in project_scores) / max(1, len(project_scores))
    registry_ready = sum(1 for p in project_scores if p.level == "registry_ready")

    partner = score_partner(load_partner(partner_raw), policy)
    copycat = score_copycat(load_partner(copycat_raw), policy)

    moat_score = clamp(0.35 * portfolio_score + 0.25 * partner.score + 0.25 * (1 - copycat.score) + 0.15 * (registry_ready / max(1, len(project_scores))))
    commercial_routes = sorted({route for p in projects for route in p.commercial_routes})
    if not commercial_routes:
        commercial_routes = ["official registry", "certification", "training", "enterprise consulting", "paid support"]

    if moat_score >= 0.78:
        strategy = "publish_ecosystemrouter_as_meta_repo_and_use_registry_certification_as_primary_moat"
    elif moat_score >= 0.55:
        strategy = "publish_with_human_partner_review_and_strengthen_registry_citation_assets"
    else:
        strategy = "delay_public_partner_program_until_attribution_and_registry_assets_are_repaired"

    return EcosystemReport(round(portfolio_score, 4), round(moat_score, 4), partner.score, copycat.score, registry_ready, strategy, project_scores, partner, copycat, commercial_routes)
