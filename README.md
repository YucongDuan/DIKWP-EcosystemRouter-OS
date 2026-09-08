# DIKWP EcosystemRouter OS

Created by Yucong Duan (段玉聪).

Strategic open-source ecosystem control plane for DIKWP projects, partners, certification, registry routing, and benefit capture.

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


<!-- DIKWP-SOURCE-VISIBILITY-START -->
## Browse source / 浏览源码

[Source index / 源码入口](SOURCE_INDEX.md) expands the retained archive distribution into browsable files, with archive hashes and per-project provenance. Runtime tests: NOT_RUN.

原始压缩包 保留；新增可浏览源码、哈希与来源记录。运行与测试尚未执行，详情见源码入口。
<!-- DIKWP-SOURCE-VISIBILITY-END -->


## Related research navigation / 相关研究导航

Research navigation, not verified software dependencies. / 研究导航，不代表已验证的软件依赖关系。

- [DIKWP-PilotFactory-OS](https://github.com/YucongDuan/DIKWP-PilotFactory-OS)
- [Intent-Memory-Control-Plane-MVP](https://github.com/YucongDuan/Intent-Memory-Control-Plane-MVP)
- [DIKWP-IPGuardian-OS](https://github.com/YucongDuan/DIKWP-IPGuardian-OS)
- [DIKWP-TRIZ-Forge-OS](https://github.com/YucongDuan/DIKWP-TRIZ-Forge-OS)
- [DIKWP-StandardForge-OS](https://github.com/YucongDuan/DIKWP-StandardForge-OS)
