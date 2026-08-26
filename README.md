# Life Policy Pilot — Health Class Estimator

Streamlit wrapper for the HealthClassEstimator life-insurance pre-underwriting and
case-triage tool. Live at https://life-insurance-health-class-predictor.streamlit.app/

The estimator is the static HTML/CSS/JS app from the
`richardparslow-commits/HealthClassEstimator` repository. `health_app.py` inlines
`index.html`, `css/styles.css`, and `js/{rules,engine,app}.js` into one
self-contained document and renders it in a component iframe — the same code that
runs in the desktop/git version.

## Updating

Copy the latest assets from `HealthClassEstimator` into this repo and redeploy:

    cp -r <HealthClassEstimator>/index.html <HealthClassEstimator>/css <HealthClassEstimator>/js .

The estimator loads rules → engine → app in order; all underwriting logic is data-driven
from `js/rules.js` (carrier rulesets) and `js/engine.js` (the rule engine).

## Running locally

    pip install -r requirements.txt
    streamlit run health_app.py
