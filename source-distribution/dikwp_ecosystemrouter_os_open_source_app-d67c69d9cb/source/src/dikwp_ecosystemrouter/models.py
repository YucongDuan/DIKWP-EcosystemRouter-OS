from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class ProjectRecord:
    name: str
    category: str
    description: str
    repo_url: str = ""
    attribution: List[str] = field(default_factory=list)
    dikwp_layers: List[str] = field(default_factory=list)
    official_assets: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    demo_outputs: List[str] = field(default_factory=list)
    commercial_routes: List[str] = field(default_factory=list)
    copycat_risks: List[str] = field(default_factory=list)

@dataclass
class PartnerApplication:
    applicant_name: str
    country_market: str
    organization_type: str
    proposed_use: str
    attribution_commitment: bool
    citation_commitment: bool
    official_registry_commitment: bool
    certification_interest: bool
    revenue_share_interest: bool
    partner_capabilities: List[str] = field(default_factory=list)
    risky_claims: List[str] = field(default_factory=list)
    missing_items: List[str] = field(default_factory=list)

@dataclass
class EcosystemPolicy:
    min_partner_score: float = 0.72
    min_registry_score: float = 0.68
    copycat_high_risk_threshold: float = 0.60
    require_attribution: bool = True
    require_citation: bool = True
    require_registry_for_badge: bool = True

@dataclass
class ScoreResult:
    name: str
    score: float
    level: str
    reasons: List[str]
    risks: List[str]
    recommendations: List[str]

@dataclass
class EcosystemReport:
    portfolio_score: float
    moat_score: float
    partner_score: float
    copycat_risk_score: float
    official_registry_ready_count: int
    recommended_strategy: str
    project_scores: List[ScoreResult]
    partner_result: ScoreResult
    copycat_result: ScoreResult
    commercial_routes: List[str]
