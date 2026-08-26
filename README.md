# Life Policy Pilot — Health Class Estimator

Streamlit wrapper for the HealthClassEstimator life-insurance pre-underwriting and
case-triage tool. Live at https://life-insurance-health-class-predictor.streamlit.app/

The estimator is the static HTML/CSS/JS app from the
`richardparslow-commits/HealthClassEstimator` repository. `health_app.py` renders
`app_embedded.html` (the CI-built single-file document) in a component iframe; if
that artifact is absent it falls back to inlining `index.html`, `css/styles.css`,
and `js/{rules,engine,app}.js` at runtime. Either way it is the same code that
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

and optionally rebuild the single-file artifact:

    cd <HealthClassEstimator> && node scripts/build-embedded.js app_embedded.html && cp app_embedded.html <this repo>/

The estimator loads rules → engine → app in order; all underwriting logic is data-driven
from `js/rules.js` (carrier rulesets) and `js/engine.js` (the rule engine).

## Running locally

    pip install -r requirements.txt
    streamlit run health_app.py
