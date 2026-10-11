# Life Policy Pilot — Health Class Estimator

Streamlit wrapper for the HealthClassEstimator life-insurance pre-underwriting and
case-triage tool. Live at https://life-insurance-health-class-predictor.streamlit.app/

The estimator is the static HTML/CSS/JS app from the
`richardparslow-commits/HealthClassEstimator` repository. `health_app.py` renders
`app_embedded.html` (the CI-built single-file document) in a component iframe; if
that artifact is absent it falls back to inlining `index.html`, `css/styles.css`,
and `js/{rules,state,engine,app}.js` at runtime. Either way it is the same code that
runs in the desktop/git version.

## Updating (automatic)

The HealthClassEstimator repository has a GitHub Actions workflow
(`.github/workflows/deploy-streamlit.yml`) that runs on every push to `main`:

1. runs the engine test suite (`npm test`),
2. builds `app_embedded.html` (`npm run build` → `scripts/build-embedded.js`),
3. pushes the built artifact plus the current assets into this repo, which
   triggers the Streamlit Cloud redeploy.

That workflow needs a personal access token (Contents read/write on this repo)
stored as the `STREAMLIT_PUSH_TOKEN` secret in the HealthClassEstimator repo.

## Updating (manual)

Copy the latest assets from `HealthClassEstimator` into this repo and redeploy:

    cp -r <HealthClassEstimator>/index.html <HealthClassEstimator>/css <HealthClassEstimator>/js .

Rebuild and copy the single-file artifact whenever the assets change:
Streamlit prefers `app_embedded.html`, so updating only the individual assets
will continue to serve the old embedded release.

    cd <HealthClassEstimator> && node scripts/build-embedded.js app_embedded.html && cp app_embedded.html <this repo>/

The estimator loads rules → state → engine → app in order; all underwriting logic is data-driven
from `js/rules.js` (carrier rulesets) and `js/engine.js` (the rule engine).

## Running locally

    pip install -r requirements.txt
    streamlit run health_app.py

## Deployment state — Release 78 follow-ups

The current assets and rebuilt embedded document are synchronized from tested
HealthClassEstimator main commit `9e069812f8274e6f6c522da05ab6dd01a1f4f82a`.
The cumulative source-derived suite passed 10,260 underwriting assertions, plus
standalone version, asset, dependency-order and single-engine checks.

This release includes the latest Quantum limits/source-conflict guards, immediate
Review completeness refresh, MOO simplified-issue driving review, and nicotine,
vital, family/driving, build/weight and criminal-date evidence validation.
Both standalone broker links open the current website contact page without
transferring estimator answers. Profile completeness remains 7 criteria, 14
partial and 3 unverified. The Python wrapper and requirements are unchanged.

The separate website owns its Contact/Concierge APIs and iframe navigation
adapters. They are not server features of this static Streamlit estimator.

The automatic cross-repository workflow requires `STREAMLIT_PUSH_TOKEN`. A green
source tests/build run does not prove deployment when that token is absent.
This release uses an explicit update to the existing deployment repository;
no credential was created or security setting changed.
