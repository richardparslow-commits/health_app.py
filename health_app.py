"""Life Policy Pilot — Health Class Estimator (Streamlit wrapper).

The estimator itself is the static HealthClassEstimator app — index.html,
css/styles.css, and js/{rules,state,engine,app}.js. Streamlit cannot serve a static
HTML/CSS/JS app from a file path, so this module inlines those assets into a
single self-contained document and renders it in a component iframe: the exact
same code that runs in the desktop/git version, byte for byte.

To update the estimator: replace the asset files in this repo with the current
ones from HealthClassEstimator, rebuild app_embedded.html, and redeploy.
All underwriting logic lives in
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
    which load_app_html() prefers. This path runs when that file is absent.

    The document produced here matches the reviewed build byte for byte apart
    from the one-line provenance stamp, which names the builder that wrote it —
    so a local run and a released artifact are the same tool, and any real
    divergence is a bug in this function. The join and the end-of-build guards
    below mirror scripts/build-embedded.js deliberately; when that builder
    changes, this one changes with it.
    """
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "css" / "styles.css").read_text(encoding="utf-8")
    rules_js = (ROOT / "js" / "rules.js").read_text(encoding="utf-8")
    state_js = (ROOT / "js" / "state.js").read_text(encoding="utf-8")
    engine_js = (ROOT / "js" / "engine.js").read_text(encoding="utf-8")
    app_js = (ROOT / "js" / "app.js").read_text(encoding="utf-8")

    # Inline the stylesheet — a relative href cannot resolve inside the iframe.
    # A function replacement, not a replacement string: re.sub reads backslash
    # escapes and \1-style group references in the replacement, so a stylesheet
    # carrying either (a CSS escape such as content: "\2192", say) would be
    # corrupted or rejected outright. scripts/build-embedded.js splits and joins
    # for the same reason.
    index = re.sub(
        r'<link rel="stylesheet"[^>]*>',
        lambda _match: "<style>\n" + css + "\n</style>",
        index,
    )
    # Capture the release version before the loader that defines it is
    # stripped, so the embedded build still exposes window.HCE_VERSION (the
    # acknowledgment record prints "App version N" — same as desktop). Mirrors
    # scripts/build-embedded.js in the HealthClassEstimator repo.
    version_match = re.search(r'var HCE_VERSION = "(\d+)"', index)
    if not version_match:
        raise RuntimeError("could not find HCE_VERSION in index.html")
    version_script = f'<script>\nwindow.HCE_VERSION = "{version_match.group(1)}"; // stamped by build_app_html\n</script>\n'
    # Drop the dynamic cache-busted script loader and inline the scripts
    # instead. Classic (non-async) inline scripts execute in document order:
    # rules -> state -> engine -> app, the load order the app depends on.
    index = re.sub(
        r"<script>\s*/\* Single cache-busting version.*?</script>",
        "",
        index,
        flags=re.S,
    )
    # Joined with a newline between blocks, matching scripts/build-embedded.js.
    inline = version_script + "\n".join(f"<script>\n{src}\n</script>" for src in (rules_js, state_js, engine_js, app_js))
    index = index.replace("</body>", inline + "\n</body>")

    # Refuse to hand a half-built document to the component: mirrors the guard in
    # scripts/build-embedded.js, so a renamed loader or an added asset file fails
    # here with a clear error instead of rendering an estimator that silently
    # runs someone else's copy of the code.
    if 'href="css/' in index or 'src="js/' in index or "Single cache-busting" in index:
        raise RuntimeError(
            "embedded build still references external assets or the cache-busting "
            "loader — update build_app_html() to match scripts/build-embedded.js"
        )
    return index


def load_app_html() -> str:
    """Return the app HTML: the CI-built single-file artifact if present,
    otherwise inline the assets at runtime (local development).

    The artifact wins because it is the file the daily consumer check verifies
    byte for byte against the reviewed build; this fallback is covered by the
    same workflow's fallback job.
    """
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
