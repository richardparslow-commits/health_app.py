"""Life Policy Pilot — Health Class Estimator (Streamlit wrapper).

The estimator is built once, in the richardparslow-commits/HealthClassEstimator
repository: `npm run release:artifact` there writes app_embedded.html (a single
self-contained document) and app_embedded.manifest.json (the sha256, byte
length, release version and builder for those bytes). Streamlit cannot serve a
static HTML/CSS/JS app from a file path, so this module hands that document to a
component iframe — and verifies the pair first, so a copy edited here fails
loudly at startup instead of rendering a tool nobody reviewed.

To update the estimator: copy the two files built there. This repository holds
no build logic and no underwriting logic — the rules and the engine live in the
canonical repository (js/rules.js, js/engine.js).

Run locally:
    pip install -r requirements.txt
    streamlit run health_app.py
"""
import hashlib
import json
import pathlib

import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parent
ARTIFACT_PATH = ROOT / "app_embedded.html"
MANIFEST_PATH = ROOT / "app_embedded.manifest.json"
BUILDER = "scripts/build-embedded.js"
FIELDS = ("artifact", "sha256", "bytes", "hce_version", "builder", "source_commit", "built_utc")
RECOVERY = (
    "rebuild the pair in the HealthClassEstimator repository and copy it here:\n"
    "    cd HealthClassEstimator && npm run release:artifact\n"
    "    cp app_embedded.html app_embedded.manifest.json <this repository>/"
)


def _refuse(problem: str) -> None:
    """Raise a RuntimeError that says what is wrong and how to fix it."""
    raise RuntimeError(problem + "\n\nTo fix it, " + RECOVERY)


def load_app_html() -> str:
    """Return the verified single-file estimator document.

    The document is the product of the canonical build, and this checks that
    before it is served: the manifest must name this file, the artifact's sha256
    and byte length must equal the ones the manifest records, the manifest must
    name the reviewed builder, and the document must carry the release version
    the manifest records. A missing,
    edited or stale pair is an error, not a fallback — the fallback this
    replaced was a second implementation of the build, and drift between the two
    was invisible until someone compared the documents byte for byte.
    """
    if not ARTIFACT_PATH.exists():
        _refuse(
            ARTIFACT_PATH.name + " is missing — the deployed estimator must come from the reviewed build."
        )
    if not MANIFEST_PATH.exists():
        _refuse(MANIFEST_PATH.name + " is missing, so " + ARTIFACT_PATH.name + " cannot be verified.")

    artifact = ARTIFACT_PATH.read_bytes()
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        _refuse(MANIFEST_PATH.name + " is not readable JSON (" + str(error) + ").")

    missing = [field for field in FIELDS if field not in manifest]
    if missing:
        _refuse(MANIFEST_PATH.name + " has no " + ", ".join(missing) + " field(s).")

    # The manifest names the file it describes; a pair from two different builds
    # can otherwise be self-consistent and still describe the wrong document.
    if manifest["artifact"] != ARTIFACT_PATH.name:
        _refuse(
            MANIFEST_PATH.name
            + " names "
            + repr(manifest["artifact"])
            + " as the artifact, but this wrapper serves "
            + ARTIFACT_PATH.name
            + ". The manifest and the document must come from the same build."
        )

    digest = hashlib.sha256(artifact).hexdigest()
    if digest != manifest["sha256"]:
        _refuse(
            ARTIFACT_PATH.name
            + " does not match its manifest: the file's sha256 is "
            + digest
            + ", the manifest records "
            + str(manifest["sha256"])
            + ". The artifact was edited outside the build."
        )
    if len(artifact) != manifest["bytes"]:
        _refuse(
            ARTIFACT_PATH.name
            + " is "
            + str(len(artifact))
            + " bytes; the manifest records "
            + str(manifest["bytes"])
            + "."
        )
    if manifest["builder"] != BUILDER:
        _refuse(
            MANIFEST_PATH.name
            + " names "
            + repr(manifest["builder"])
            + " as the builder; only "
            + BUILDER
            + " output may be served."
        )

    text = artifact.decode("utf-8")
    version = manifest["hce_version"]
    if 'window.HCE_VERSION = "' + str(version) + '"' not in text:
        _refuse(
            ARTIFACT_PATH.name
            + ' does not carry window.HCE_VERSION = "'
            + str(version)
            + '" as the manifest records.'
        )
    return text


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
