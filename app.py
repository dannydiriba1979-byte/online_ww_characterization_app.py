import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE_PATH = os.path.join(HERE, "influent_model_bundle.joblib")

st.set_page_config(
    page_title="AquaEstimate | Influent AI",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --navy:#102a43; --blue:#167dba; --teal:#168b83; --pale:#edf7fb; --ink:#20364a; --muted:#64798b; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:linear-gradient(180deg,#f4f9fc 0%,#ffffff 44%,#f7fbfc 100%); color:var(--ink); }
.block-container { max-width:1200px; padding-top:1.7rem; padding-bottom:3rem; }
.hero { background:linear-gradient(120deg,#102a43 0%,#145b7b 58%,#168b83 100%); color:white; padding:2rem 2.2rem; border-radius:22px; margin-bottom:1.3rem; box-shadow:0 14px 34px rgba(16,42,67,.14); }
.eyebrow { font-size:.76rem; text-transform:uppercase; letter-spacing:.16em; font-weight:700; color:#a9e7e0; margin-bottom:.65rem; }
.hero h1 { font-family:'Manrope',sans-serif; font-size:clamp(1.8rem,3vw,2.7rem); line-height:1.12; color:white; margin:0 0 .7rem 0; font-weight:800; }
.hero p { font-size:1rem; line-height:1.6; color:#e3f2f7; max-width:760px; margin:0; }
.section-title { font-family:'Manrope',sans-serif; color:#102a43; font-size:1.25rem; font-weight:800; margin:.5rem 0 .25rem 0; }
.section-subtitle { color:#64798b; font-size:.9rem; margin-bottom:1rem; }
.input-panel { background:white; border:1px solid #dbe8ef; border-radius:18px; padding:1.2rem 1.35rem .7rem 1.35rem; box-shadow:0 7px 22px rgba(16,42,67,.045); }
.result-card { background:white; border:1px solid #dce8ef; border-radius:18px; padding:1.25rem 1.2rem; min-height:225px; box-shadow:0 7px 22px rgba(16,42,67,.045); }
.result-head { color:#536d80; text-transform:uppercase; letter-spacing:.08em; font-weight:700; font-size:.75rem; margin-bottom:.55rem; }
.result-name { font-family:'Manrope',sans-serif; font-size:1.35rem; font-weight:800; color:#102a43; margin-bottom:.2rem; }
.result-value { font-family:'Manrope',sans-serif; font-size:2rem; font-weight:800; letter-spacing:-.04em; color:#167dba; line-height:1.25; margin:.8rem 0 .4rem 0; overflow-wrap:anywhere; }
.result-unit { color:#64798b; font-size:.85rem; }
.status-pill { display:inline-block; border-radius:99px; padding:.28rem .65rem; font-size:.72rem; font-weight:700; background:#e8f5f2; color:#146b62; margin-top:.55rem; }
.status-warn { background:#fff3dc; color:#8a5b09; }
.status-bad { background:#fde9e7; color:#9d3029; }
.small-note { color:#64798b; font-size:.82rem; line-height:1.5; }
div.stButton > button { background:linear-gradient(90deg,#167dba,#168b83); color:white; border:0; border-radius:12px; padding:.72rem 1rem; font-weight:700; min-height:3rem; }
div.stButton > button:hover { color:white; border:0; filter:brightness(1.04); }
[data-testid="stMetric"] { background:#f6fbfd; padding:.75rem; border-radius:12px; }
hr { border-color:#dce8ef; }
@media(max-width:700px){ .hero{padding:1.4rem;border-radius:16px}.result-card{min-height:190px}.block-container{padding-left:1rem;padding-right:1rem} }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_bundle():
    if not os.path.exists(BUNDLE_PATH):
        raise FileNotFoundError("Model bundle not found. Keep influent_model_bundle.joblib beside app.py.")
    return joblib.load(BUNDLE_PATH)

st.markdown("""
<div class="hero">
  <div class="eyebrow">Wastewater intelligence · Influent only</div>
  <h1>AquaEstimate</h1>
  <p>Estimate BOD₅, total nitrogen (TN), and total phosphorus (TP) from routine influent measurements. Enter COD and, when available, TSS; each parameter has its own dedicated output panel.</p>
</div>
""", unsafe_allow_html=True)

bundle = load_bundle()

st.markdown('<div class="section-title">01 · Routine measurements</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Use results from the same influent sample. All concentrations must be in mg/L.</div>', unsafe_allow_html=True)

with st.container(border=True):
    c1, c2, c3 = st.columns([1, 1, 1.2], gap="large")
    with c1:
        cod = st.number_input("Chemical oxygen demand · COD", min_value=0.0, max_value=100000.0, value=500.0, step=10.0, help="Required for all three prototype models.")
        st.caption("mg/L · Required input")
    with c2:
        tss_available = st.toggle("TSS result available", value=True, help="TN and TP models require COD and TSS.")
        tss = st.number_input("Total suspended solids · TSS", min_value=0.0, max_value=100000.0, value=350.0, step=10.0, disabled=not tss_available, help="Required by the prototype TN and TP models.")
        st.caption("mg/L · Required for TN and TP" if tss_available else "TSS not supplied · TN and TP will remain unavailable")
    with c3:
        st.markdown("**Your measurement plan**")
        st.markdown("<div class='small-note'>BOD₅ uses COD only. TN and TP use COD + TSS. The estimator will not ask you to enter a laboratory result for the parameter being estimated.</div>", unsafe_allow_html=True)
        estimate = st.button("Calculate estimated parameters  →", type="primary", use_container_width=True)

if "has_estimate" not in st.session_state:
    st.session_state.has_estimate = False
if estimate:
    st.session_state.has_estimate = True
    st.session_state.last_cod = float(cod)
    st.session_state.last_tss = float(tss) if tss_available else None

# Results persist after calculation; the panels remain visible before and after the first run.
if st.session_state.has_estimate:
    active_cod = st.session_state.last_cod
    active_tss = st.session_state.last_tss
else:
    active_cod = None
    active_tss = None

st.markdown('<div class="section-title">02 · Estimated influent parameters</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Each result appears in its own panel. Values shown after calculation are model estimates, not laboratory measurements.</div>', unsafe_allow_html=True)

cards = st.columns(3, gap="medium")
targets = [
    {"key":"BOD5", "name":"BOD₅", "full":"Biochemical oxygen demand · 5-day", "inputs":"COD", "color":"#167dba", "warning":"Candidate model · validate before reducing BOD₅ testing."},
    {"key":"TN", "name":"TN", "full":"Total nitrogen", "inputs":"COD + TSS", "color":"#168b83", "warning":"Research only · do not replace TN laboratory testing."},
    {"key":"TP", "name":"TP", "full":"Total phosphorus", "inputs":"COD + TSS", "color":"#6b72b8", "warning":"Research only · do not replace TP laboratory testing."},
]
for col, target in zip(cards, targets):
    with col:
        info = bundle["models"][target["key"]]
        can_predict = active_cod is not None and all(f == "COD" or (f == "TSS" and active_tss is not None) for f in info["features"])
        if can_predict:
            values = {"COD": active_cod, "TSS": active_tss}
            X = pd.DataFrame([{f: values[f] for f in info["features"]}])
            prediction = float(info["estimator"].predict(X)[0])
            if np.isfinite(prediction):
                value_html = f"{prediction:,.2f}"
                negative = prediction < 0
            else:
                value_html = "Unavailable"
                negative = True
        else:
            value_html = "— —"
            negative = False
        st.markdown(f"""
        <div class="result-card" style="border-top:5px solid {target['color']};">
          <div class="result-head">Model output</div>
          <div class="result-name">{target['name']}</div>
          <div class="small-note">{target['full']}</div>
          <div class="result-value" style="color:{target['color']};">{value_html}</div>
          <div class="result-unit">mg/L</div>
          <div class="status-pill {'status-warn' if target['key']=='BOD5' else 'status-bad'}">{'Candidate model' if target['key']=='BOD5' else 'Research only'}</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"Required inputs: {target['inputs']}")
        if not st.session_state.has_estimate:
            st.info("Enter the routine measurements above and select Calculate to display this estimate.")
        elif not can_predict:
            st.warning("Not estimated: this model requires TSS as well as COD.")
        elif negative:
            st.error("The model returned an invalid or negative estimate. Do not use this value; review the model and input data.")
        else:
            st.warning(target["warning"])

if st.session_state.has_estimate:
    output = {"COD_input_mg_L": active_cod, "TSS_input_mg_L": active_tss}
    for target in targets:
        info = bundle["models"][target["key"]]
        if active_cod is not None and all(f == "COD" or (f == "TSS" and active_tss is not None) for f in info["features"]):
            X = pd.DataFrame([{f: {"COD":active_cod,"TSS":active_tss}[f] for f in info["features"]}])
            pred = float(info["estimator"].predict(X)[0])
            output[target["key"] + "_estimate_mg_L"] = pred if np.isfinite(pred) and pred >= 0 else np.nan
        else:
            output[target["key"] + "_estimate_mg_L"] = np.nan
    st.download_button("Download this estimate as CSV", pd.DataFrame([output]).to_csv(index=False).encode("utf-8"), file_name="wastewater_influent_estimates.csv", mime="text/csv")

st.divider()
st.markdown('<div class="section-title">03 · Validation and responsible use</div>', unsafe_allow_html=True)
st.markdown("""
<div class="small-note">These are prototype models trained from the supplied 2019 and 2020 workbooks. A chronological holdout evaluation within the 2020 workbook produced the following results; the TN and TP test sets were very small.</div>
""", unsafe_allow_html=True)
metrics = pd.DataFrame({
    "Parameter": ["BOD₅", "TN", "TP"],
    "Inputs": ["COD", "COD + TSS", "COD + TSS"],
    "Test samples": [62, 4, 11],
    "MAE (mg/L)": [34.742, 8.786, 0.727],
    "RMSE (mg/L)": [45.262, 10.703, 0.901],
    "R²": [0.855, -5.476, -1.124],
})
st.dataframe(metrics, use_container_width=True, hide_index=True)
with st.expander("Read limitations before using estimates"):
    st.markdown("""
- This application estimates **wastewater influent** concentrations only.
- Use COD and TSS values from the same sample and enter concentrations in mg/L.
- BOD₅ is a candidate for further prospective validation; this result alone does not justify stopping BOD₅ testing.
- TN and TP are research-only. Their small holdout samples and negative R² values do not support replacing laboratory analyses.
- Do not use predictions alone for regulatory reporting, compliance decisions, or safety-critical process control.
- Continue paired laboratory sampling to quantify error and detect changes in influent characteristics.
- Example input values are prefilled for convenience and are not actual plant measurements.
""")
st.caption("AquaEstimate · Research prototype · The app runs predictions locally within its hosting environment and does not independently verify samples.")
