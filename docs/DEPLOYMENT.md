# Deployment and maintenance

The intended public dashboard URL is `https://portfolio.chrisdelgado.workers.dev/ai-cost-efficiency/`. Its prepared case-study entry is `/projects/ai-cost-efficiency/`, and the prepared portfolio homepage features this project first. Cloudflare publication is deferred to the owner's separate portfolio project; see the [current handoff](PORTFOLIO_HANDOFF.md).

The source of the dashboard is this repository. The deployment owner is the existing [Chris-Delgado-Portfolio-Career-Website](https://github.com/GlassHouse97/Chris-Delgado-Portfolio-Career-Website) Astro repository. Its Cloudflare Workers Builds connection builds the production branch. No new hosting account, Site registration, Worker, secret, or API credential is required.

## Update the published copy

1. Regenerate data only when changing the synthetic scenario. Run the data validator, Python tests, JavaScript tests, and package check described in the root README.
2. Run `npm run build` in this repository.
3. Copy the checked dashboard into the existing portfolio checkout with:

```sh
node scripts/sync-portfolio.mjs "../Portfolio Website"
```

The helper copies only `dashboard/` into `public/ai-cost-efficiency/` and writes a source manifest with SHA-256 file hashes. It does not change existing portfolio pages, remove other assets, commit, push, or deploy.

4. In the portfolio checkout, run `npm run build`. Review changes to the public assets, homepage, and case-study page.
5. Commit and push the intended changes to the two repositories. The portfolio's production push invokes the existing Cloudflare build. Check the new commit's **Workers Builds: portfolio** result and the live URLs. A push alone is not proof of deployment.
6. Verify both download links and compare their SHA-256 hashes with the release files here. The downloads are `mru-portfolio-project.zip` and `mru-quick-challenge.zip` under `/ai-cost-efficiency/downloads/`.

The copied app uses relative asset URLs and supports static hosts. `npm run build` also emits `dist/` for standalone static hosting. No server runtime or database is needed. The learner ZIPs work independently of hosting.

## Rollback

Use a normal Git revert of the relevant portfolio release commit and let the existing Cloudflare build publish the reverted assets. Retain the matching analysis repository commit for reproducibility. Never force-push over unrelated portfolio work.
