# Portfolio publication handoff

October 22, 2026. The owner requested that Cloudflare publication be handled in a separate portfolio project. Deployment work stopped at that request.

## Ready in this repository

- `dashboard/` contains the completed static application, source JSON, and both learner ZIPs. No API key, backend, or account is required to run it.
- `release/mru-quick-challenge.zip` and `release/mru-portfolio-project.zip` are the standalone exercises. Both include offline HTML guides and exclude completed solutions.
- `npm run dev` serves the dashboard at `http://127.0.0.1:4327/`.
- `npm run build` prepares `dist/`. Copy that static output into the portfolio at `/ai-cost-efficiency/`, or use `node scripts/sync-portfolio.mjs "../Portfolio Website"` from this repository.
- `docs/ANALYSIS.md` contains the completed case study; `docs/VALIDATION.md` records validation. All 18 automated tests and the GitHub validation workflow passed.

## Portfolio integration already prepared

The existing portfolio repository is `GlassHouse97/Chris-Delgado-Portfolio-Career-Website`. Its local checkout is the sibling folder `Portfolio Website`.

Before publication was deferred, the integration was pushed in commit `1c09f507e5ac225bfc01709a56454a1e2dab6881`, with asset-manifest normalization in `e81f3cf333898b65f0a4dff1e80e938dd17097da`:

- `src/pages/index.astro`: AI dashboard is the primary homepage action and first featured project; existing projects remain.
- `src/pages/projects/ai-cost-efficiency.astro`: case study and both learner download links.
- `src/layouts/ProjectLayout.astro`: optional primary dashboard link and narrow-screen table containment.
- `public/ai-cost-efficiency/`: copied dashboard assets, downloads, and SHA-256 source manifest.

The pushes triggered the pre-existing Cloudflare Workers Builds integration. The build for `e81f3cf` failed. At the last check, the existing homepage still served the previous site, and both new routes returned 404. **The new dashboard has not been verified as deployed.** The GitHub check links to Cloudflare's private build log; the available browser session requires Cloudflare sign-in to read that log.

## Local deployment changes left unpushed

The portfolio production branch had no Wrangler configuration. A supported static-assets configuration was prepared locally, but the owner deferred deployment before it was committed or pushed:

- New `wrangler.jsonc`: existing Worker name `portfolio`, static assets from `dist/`, normal 404 handling.
- `package.json` and `package-lock.json`: pinned Wrangler 4.152.0 and `deploy` / `deploy:check` scripts.
- `.gitignore`: excludes local `.wrangler/` state.
- `README.md`: documents the Worker deployment and new project routes.

`npm run deploy:check` passed locally and found 42 built static files. This validates the proposed configuration; it does not establish the cause of the remote build failure or prove a successful deployment. Review the actual Cloudflare build log before completing publication.

## Publication paths to verify later

| Purpose | Intended path |
| --- | --- |
| Main dashboard | `/ai-cost-efficiency/` |
| Portfolio case study | `/projects/ai-cost-efficiency/` |
| Deeper learner download | `/ai-cost-efficiency/downloads/mru-portfolio-project.zip` |
| Quick learner download | `/ai-cost-efficiency/downloads/mru-quick-challenge.zip` |

When the separate portfolio project publishes successfully, verify the live filters, both download hashes, the homepage's featured link, and the production build status. Then update this repository's README from “ready for portfolio deployment” to the verified live dashboard link.
