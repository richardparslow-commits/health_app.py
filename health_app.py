"""Life Policy Pilot — Health Class Estimator (Streamlit wrapper).

The estimator itself is the static HealthClassEstimator app — index.html,
css/styles.css, and js/{rules,engine,app}.js. Streamlit cannot serve a static
HTML/CSS/JS app from a file path, so this module inlines those assets into a
single self-contained document and renders it in a component iframe: the exact
same code that runs in the desktop/git version, byte for byte.

To update the estimator: replace the asset files in this repo with the current
ones from HealthClassEstimator and redeploy. All underwriting logic lives in
js/rules.js (carrier data) and js/engine.js (the rule engine); nothing
underwriting-related lives in this Python file.

Run locally:
    pip install -r requirements.txt
    streamlit run health_app.py
"""
import pathlib
import re

import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parent


def build_app_html() -> str:
    """Inline the static assets into a single self-contained HTML document.

    Local-development fallback. The GitHub Actions workflow in the
    HealthClassEstimator repo builds the same document ahead of time
    (scripts/build-embedded.js) and pushes it here as app_embedded.html,
    which load_app_html() prefers.
    """
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "css" / "styles.css").read_text(encoding="utf-8")
    rules_js = (ROOT / "js" / "rules.js").read_text(encoding="utf-8")
    engine_js = (ROOT / "js" / "engine.js").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    # Inline the stylesheet — a relative href cannot resolve inside the iframe.
    index = re.sub(
        r'<link rel="stylesheet"[^>]*>',
        "<style>\n" + css + "\n</style>",
        index,
    )
    # Drop the dynamic cache-busted script loader and inline the scripts
    # instead. Classic (non-async) inline scripts execute in document order:
    # rules -> engine -> app, the load order the app depends on.
    index = re.sub(
        r"<script>\s*/\* Single cache-busting version.*?</script>",
        "",
        index,
        flags=re.S,
    )
    inline = "".join(f"<script>\n{src}\n</script>" for src in (rules_js, engine_js, app_js))
    index = index.replace("</body>", inline + "\n</body>")
    return index


def load_app_html() -> str:
    """Return the app HTML: the CI-built single-file artifact if present,
    otherwise inline the assets at runtime (local development)."""
    embedded = ROOT / "app_embedded.html"
    if embedded.exists():
        return embedded.read_text(encoding="utf-8")
    return build_app_html()


st.set_page_config(
    page_title="Health Class Estimator — Life Policy Pilot",
    page_icon="🩺",
    layout="wide",
)

# Hide Streamlit's own chrome so the page is the estimator itself.
st.markdown(
    """
    <style>
      #MainMenu, footer { visibility: hidden; }
      [data-testid="stHeader"] { display: none; }
      .block-container { max-width: 100%; padding-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Preliminary, non-binding underwriting-lane estimate for producer case triage. "
    "Not a medical diagnostic tool; does not issue insurance or replace a carrier "
    "underwriter's decision."
)

try:
    st.components.v1.html(load_app_html(), height=2400, scrolling=True)
except TypeError:  # older Streamlit releases without the scrolling parameter
    st.components.v1.html(load_app_html(), height=2400)
