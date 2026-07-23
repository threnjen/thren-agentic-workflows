# Discovery Context: Client Deliverable Package — Pilot Engagement (SSX SurfaceCapture)

Context gathered during planning that downstream agents (`@phase-refiner`, `@phase-execute`) need but cannot derive from this repository.

**Note**: The agent set itself is engagement-agnostic (see `PROJECT_ROADMAP.md`). Everything below is the **pilot engagement** the tool will first run against — it parameterizes the tool; it does not define it.

## The Pilot Engagement

Copper Forge, LLC upgraded SUPERSTRUCTURES (SSX) SurfaceCapture — a facade-inspection system — from .NET Core 2.1 / .NET Standard 2.0 to .NET 10 under SOW No. 1 (MSA dated 2026-06-22). Two solutions:

1. **Backend/web** (`SSX.AIM.SurfaceCapture`): SurfaceCapture.Web (MVC, Azure AD auth), SurfaceCapture.API (JWT REST API, per-project multi-tenant Azure SQL via %PROJECTNAME% connection-string templating), SurfaceCapture.Register (shared DI composition root), ImageResolution.WebJob (queue-driven image resizing to blob), Notification.Function (completion/failure emails). **No functional changes intended** — pure modernization.
2. **Desktop** (`SSX.AIM.SurfaceCapture.Uploader`): Uploader + GigaPixel Converter. Modernization **plus functional changes**: single ClickOnce installer for both apps; prerequisite installs removed (old .NET, Python, LibVips, AzCopy — LibVips/AzCopy now bundled); Python/KRO support removed (TIFF-only); KRO upload option removed from UI; gigapixel Azure round-trip replaced with local handoff to the Converter; conversion made asynchronous (operator keeps working; app may close during conversion where feasible); mosaic pipeline preserved.

## Repositories (four, separate histories)

Old and new copies of each solution are kept as **separate repos** — comparisons are cross-repo, not git-diff-based. (Exact local paths TBD during Phase 01.)

## Source Documents

| Document | Path | Authority |
|---|---|---|
| Internal client-deliverables spec | `~/github_repos/copperforge/ssx-surface-capture/client-deliverables-spec.md` | Defines the 7-item deliverable package + self-review requirement |
| Original engagement brief (PDF) | `~/github_repos/copperforge/ssx-surface-capture/SC_Solution_Upgrade_NET10_Engagement_Brief.pdf` | Superseded on scope (desktop apps added later); Part II remains a good system reference and seed for the business design doc |
| SOW No. 1 | `~/github_repos/copperforge/cf-ops-company/projects/ssx/copper-forge-ssx-sow1.md` | Authoritative: scope §3, deliverables §4, exclusions §9, acceptance criteria §10 |

## Client-Spec Deliverables → Production Mapping

1. **Proof of spec compliance** → SOW §10 acceptance-criteria walkthrough + §3.3 test-evidence
2. **Business design doc** → plain-language narrator (brief Part II as seed)
3. **Setup/operations doc** → §3.4 publishing docs + prerequisites + maintenance + known-limitations disclaimers
4. **Findings report (business-framed)** → comparative audits old-vs-new, synthesized to business risk; includes cloud/cost observations
5. **Out-of-scope issues list** → severity-rated register split from audit output, routed via SOW §9 exclusions
6. **Specification of intended behavior** ("warranty" doc) → behavior-spec agent seeded by SOW §3.3 behaviors
7. **Audit trail of our own work** → same scans run on new repos, framed as "our deliverable passes the categories we flagged"

Plus: executive summary, branded PDF assembly, and a pre-handoff client-perspective self-review (open task in the spec).

## Key Decisions Made During Planning

- **Audience is non-technical** — business-meaning first, technical evidence in appendices.
- **One bound package, two value stories**: backend "modernized, nothing changed"; desktop "modernized and improved."
- Raw everything-diff rejected in favor of **subsystem-by-subsystem change narrative** (reads as value, not churn).
- **PDF pipeline**: none exists; to be standardized in the assembly phase. Copper Forge branding template asset needed (existence unconfirmed — open question).
- **Delivery to the client's own repo**; repo permanence is the client's responsibility.
- User docs (usage/screens) produced by the team separately — excluded from this agent set.
- **Prerequisites before any comparison** (user-directed): full docs-writer pass and built code-review-graph on each of the four repos.

## Open Questions

- Branding template asset (logo/colors/cover): exists, or created in Phase 06?
- One-click installer prerequisites (OS, runtimes) — flagged unconfirmed in the deliverables spec; resolve during operational-docs phase.
- Local paths of the four repos.
