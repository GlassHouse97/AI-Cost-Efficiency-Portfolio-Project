# Portfolio connection handoff

The completed project is ready to be linked from the owner's separate portfolio website. The dashboard is hosted independently on Google Cloud Run; no Cloudflare deployment is required for this repository.

## Links for the portfolio card

| Purpose | Link |
| --- | --- |
| Primary action: live dashboard | [Open dashboard](https://ai-cost-efficiency-860922042669.us-east1.run.app) |
| Source and project overview | [GitHub repository](https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project) |
| Completed case study | [Executive summary](https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/blob/main/SOLUTION/TRACKS/portfolio-project/EXECUTIVE_SUMMARY.md) |
| Quick learner exercise | [Download ZIP](https://ai-cost-efficiency-860922042669.us-east1.run.app/downloads/mru-quick-challenge.zip) |
| Quick completed solution | [Excel solution guide](https://github.com/GlassHouse97/AI-Cost-Efficiency-Portfolio-Project/blob/main/SOLUTION/TRACKS/quick-challenge/README.md) |
| Deeper learner exercise | [Download ZIP](https://ai-cost-efficiency-860922042669.us-east1.run.app/downloads/mru-portfolio-project.zip) |

**Suggested title:** AI Cost Efficiency & Workflow Value

**Suggested description:** An interactive business case tracing AI token spending through staff effort, rework, and campaign profitability. Explore four synthetic campaigns, test baseline assumptions, and inspect a reproducible analysis with two standalone learner exercises and a self-contained worked Excel answer for the quick track.

**Suggested image:** [Company overview](../../SOLUTION/TRACKS/portfolio-project/visualizations/01_company_overview.jpg). Additional evidence panels are in [SOLUTION/TRACKS/portfolio-project/visualizations/](../../SOLUTION/TRACKS/portfolio-project/visualizations/), with their filter settings and capture provenance.

Make the live dashboard the primary action and GitHub the supporting source link. Keep the learning exercises available from the repository and the dashboard's learner section. The README already explains the business problem, guiding questions, supported answers, and reproduction steps.

## Existing portfolio work to review in the separate project

Before the owner deferred Cloudflare publication, portfolio integration was pushed to `GlassHouse97/Chris-Delgado-Portfolio-Career-Website` in commits `1c09f507e5ac225bfc01709a56454a1e2dab6881` and `e81f3cf333898b65f0a4dff1e80e938dd17097da`. It included a homepage feature, case-study page, and copied static dashboard. The existing Cloudflare build failed at that time, and the new routes were not live. Local Wrangler configuration changes were left unpushed in that separate checkout.

That is historical handoff information, not a current Cloudflare health check. Review those pending changes in the portfolio project, and update its primary dashboard action to the Cloud Run URL above. This repository's current release does not edit or deploy that website.

The optional `TECHNICAL/scripts/sync-portfolio.mjs` helper can still copy static assets to a compatible checkout if self-hosting is deliberately chosen later. It is unnecessary when simply linking to Cloud Run and is not called by build, validation, or deployment.
