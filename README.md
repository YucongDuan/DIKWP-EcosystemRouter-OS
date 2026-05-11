# DIKWP EcosystemRouter OS

**Strategic open-source ecosystem control plane for DIKWP projects, partners, certification, registry routing, and benefit capture.**

This project is designed for Yucong Duan / DIKWP ecosystem strategy in China and global markets. It does not expose critical industry device adapters or operational gateways. Instead, it provides a public, GitHub-ready strategic layer that turns DIKWP reuse into attribution, citation, registry entry, partner routing, certification, training, and commercial opportunity.

## Core idea

Code can be copied. A canonical ecosystem cannot be honestly copied.

DIKWP EcosystemRouter OS helps build the non-code moat around DIKWP:

- canonical project registry
- partner application routing
- project portfolio positioning
- ecosystem moat scoring
- copycat risk analysis
- certification program scaffolding
- commercial package catalog
- GitHub release and launch plan
- attribution and citation discipline

## What it does

The CLI reads an ecosystem manifest and partner applications, then produces:

- official registry seed
- portfolio scorecard
- partner routing decision
- moat scorecard
- copycat response playbook
- commercial package catalog
- training and certification catalog
- public roadmap and partner onboarding checklist

## Install

```bash
pip install -e .
```

## Run demo

```bash
dikwp-ecosystemrouter evaluate examples/sample_ecosystem_manifest.json \
  --partner examples/sample_partner_application.json \
  --copycat examples/sample_copycat_application.json \
  --policy configs/default_policy.json \
  --out outputs/demo
```

## Static audit

```bash
dikwp-ecosystemrouter static-audit src \
  --out outputs/demo/static_boundary_audit_report.json
```

## Boundary

This is a strategic registry and ecosystem routing tool. It is not legal advice, not a trademark registration, not a patent filing, not a certification authority by itself, and not a guarantee of commercial revenue. Formal trademark, copyright, patent, procurement, legal, and partner agreements require professional review.

## Attribution

This package is designed to preserve and amplify attribution to Yucong Duan and the DIKWP model. See `NOTICE` and `CITATION.cff`.
