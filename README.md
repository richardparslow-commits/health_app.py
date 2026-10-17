# Life Policy Pilot — Health Class Estimator

Streamlit wrapper for the HealthClassEstimator life-insurance pre-underwriting and
case-triage tool. Live at https://life-insurance-health-class-predictor.streamlit.app/

The estimator itself lives in `richardparslow-commits/HealthClassEstimator`. This
repository holds only the wrapper and the built document: `app_embedded.html`, a
single self-contained file, and `app_embedded.manifest.json`, which records its
sha256, byte length, release version and the builder that produced it.
`health_app.py` serves the document in a component iframe after verifying it
against the manifest. There is no build logic here and no underwriting logic —
the rules and the engine live in the canonical repository (`js/rules.js`,
`js/engine.js`).

## Updating (automatic)

The canonical repository's `.github/workflows/deploy-streamlit.yml` builds the
pair and pushes it here on every push to `main`, which triggers the Streamlit
Cloud redeploy. That workflow needs a personal access token (Contents read/write
on this repository) stored as the `STREAMLIT_PUSH_TOKEN` secret there.

## Updating (manual)

Copy the pair, nothing else:

    cd <HealthClassEstimator> && npm run release:artifact
    cp <HealthClassEstimator>/app_embedded.html <HealthClassEstimator>/app_embedded.manifest.json .

Commit and push; Streamlit Cloud redeploys on the push.

## Verification

The document is embedded with `st.iframe`, Streamlit's supported way to serve an
HTML string, and this repository requires `streamlit>=1.66`. It used to call
`st.components.v1.html`, which Streamlit removes after 2026-06-01 — an upgrade
would have broken the app with no change here, which is why the canonical
repository now runs the staged app through Streamlit's real runtime before any
push.

At startup — and on every Streamlit rerun — `health_app.py` refuses to serve a
pair unless the manifest names `app_embedded.html` as its artifact, the
artifact's sha256 and byte length match the manifest, the manifest names
`scripts/build-embedded.js` as the builder, and the document carries the release
version the manifest records. A missing or edited pair is a
loud error naming the command that fixes it, never a silently different tool:
this repository used to inline loose assets when the artifact was missing, and
that second implementation of the build drifted from the reviewed one in three
places before it was removed.

The daily `Check the live consumers against the build` workflow in the canonical
repository compares this artifact with a fresh build **byte for byte** and
exercises this wrapper the way Streamlit does: the published pair must load, and
a tampered artifact, a missing artifact, a missing manifest, a manifest that
names a different file as its artifact and a manifest whose release version lies
must all be refused.

One residual risk, stated plainly: an artifact edited by hand *together with* a
hand-regenerated manifest is self-consistent and passes at startup. Regenerating
the manifest requires the reviewed builder's own output, so that case is what the
byte-for-byte fresh-build comparison exists to catch.

## Running locally

    pip install -r requirements.txt
    streamlit run health_app.py
