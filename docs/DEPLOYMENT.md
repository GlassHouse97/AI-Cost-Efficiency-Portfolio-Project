# Cloud Run deployment

The dashboard is hosted at **[ai-cost-efficiency-860922042669.us-east1.run.app](https://ai-cost-efficiency-860922042669.us-east1.run.app)**. It runs independently of the portfolio website. The owner will connect the completed repository and live dashboard from that separate project.

| Setting | Value |
| --- | --- |
| Google Cloud project | `chris-delgados-data-portfolio` |
| Service | `ai-cost-efficiency` |
| Region | `us-east1` |
| Public access | Unauthenticated, public synthetic demo |
| Runtime | Node.js 24, non-root container user |
| Resources | 1 CPU, 256 MiB, concurrency 80, 60-second request timeout |
| Scaling | Minimum 0, maximum 2 instances |
| Health endpoint | `/health` |

The browser performs the calculations against bundled synthetic data. The small Node server only serves static assets and downloads; it has no database, API key, session state, or model API calls. Minimum zero allows the service to scale down when idle. Hosting, build, and artifact-storage charges follow the project's Google Cloud billing; the instance limit is not a spending cap.

## Validate before deployment

Run from this repository with Node.js 22+ and Python 3.10+:

```sh
python scripts/validate_data.py
python -m unittest discover -s tests -p "test_data.py" -v
python scripts/analyze_case_study.py
npm test
python scripts/package_learners.py --check
npm run build
```

`npm run dev` serves loopback port 4327. `npm start` runs the production server on `0.0.0.0` using `PORT` (default 8080), matching the [Cloud Run container contract](https://docs.cloud.google.com/run/docs/container-contract). The health path is `/health`; Google reserves some paths ending in `z`, so `/healthz` is deliberately avoided. See [reserved URL paths](https://docs.cloud.google.com/run/docs/known-issues#reserved-url-paths).

## Deploy manually

Use an authenticated Google Cloud CLI identity with access to this project. The Run, Cloud Build, and Artifact Registry APIs are required. Review the upload list before deploying:

```sh
gcloud meta list-files-for-upload
```

The allowlist includes only `dashboard/`, `scripts/server.mjs`, `Dockerfile`, and the two ignore files. It excludes the requirements document, Git history, learner authoring sources, and local credentials. `Dockerfile` copies only the dashboard and server into the image.

```sh
gcloud run deploy ai-cost-efficiency --source . --project chris-delgados-data-portfolio --region us-east1 --allow-unauthenticated --min-instances 0 --max-instances 2 --memory 256Mi --cpu 1 --concurrency 80 --timeout 60 --port 8080 --quiet
```

[Source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code) builds the supplied Dockerfile with Cloud Build and stores the image in Artifact Registry. No local Docker daemon is required. This is a manual deployment; the GitHub workflow validates commits and does not deploy them.

## Verify the release

```sh
gcloud run services describe ai-cost-efficiency --project chris-delgados-data-portfolio --region us-east1 --format="yaml(status.url,status.latestReadyRevisionName,status.traffic)"
```

Confirm a ready revision receives 100% of traffic, then verify the public root, `/health`, scripts, dataset, and both learner downloads. Compare the downloaded ZIP SHA-256 values with `release/`. Open the public dashboard and check the all-company totals and the Campaigns 1 + 2 filter. A successful Git push alone does not establish a deployment.

| Download | SHA-256 |
| --- | --- |
| `mru-quick-challenge.zip` | `6a7969604ddcc6c9d490f55e4a6b4ae6bea65f3fc8850475a0892c36aef779f7` |
| `mru-portfolio-project.zip` | `10d2b0febfafc17c44e479ee75f795a17c1d870143e0f5630dc516f21bfb1465` |

The release record is in [VALIDATION.md](VALIDATION.md). The service also has Google's equivalent hashed hostname; the readable project-number URL above is the portfolio link.

## Rollback

List available revisions, identify the last verified revision, and route traffic to that explicit revision:

```sh
gcloud run revisions list --service ai-cost-efficiency --project chris-delgados-data-portfolio --region us-east1
gcloud run services update-traffic ai-cost-efficiency --to-revisions PREVIOUS_READY_REVISION=100 --project chris-delgados-data-portfolio --region us-east1
```

Replace the placeholder with a real verified revision. Alternatively, revert the relevant source commit normally, validate it, and deploy it. Keep Git source and the deployment record aligned; do not force-push over unrelated work.
