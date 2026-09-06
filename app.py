import streamlit as st
import pandas as pd
import numpy as np
import shap
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="EcoOptiX", layout="wide", page_icon="🌱")

FEATURES = [
    "Server_Utilization", "Workload_Intensity", "Ambient_Temperature",
    "Cooling_Intensity", "Cooling_Setpoint", "Humidity"
]
TARGETS = ["Energy_kWh", "Water_Litres", "Carbon_kg", "Performance_Score"]

SLIDER_LABELS = {
    "Server_Utilization": "Server Utilization (%)",
    "Workload_Intensity": "Workload Intensity (%)",
    "Ambient_Temperature": "Ambient Temperature (°C)",
    "Cooling_Intensity": "Cooling Intensity (%)",
    "Cooling_Setpoint": "Cooling Setpoint (°C)",
    "Humidity": "Humidity (%)",
}

DEFAULT_STATE = {
    "Server_Utilization": 82.0,
    "Workload_Intensity": 85.0,
    "Ambient_Temperature": 36.0,
    "Cooling_Intensity": 78.0,
    "Cooling_Setpoint": 21.0,
    "Humidity": 62.0,
}

MIN_PERFORMANCE = 96.0


# ---------------------------------------------------------------------
# 1. SYNTHETIC DATA-CENTRE TELEMETRY  (exact logic from your Colab)
# ---------------------------------------------------------------------
@st.cache_data
def generate_synthetic_data(N=5000, seed=42):
    rng = np.random.RandomState(seed)

    server_utilization = rng.uniform(20, 100, N)
    workload_intensity = rng.uniform(20, 100, N)
    ambient_temperature = rng.uniform(18, 42, N)
    cooling_intensity = rng.uniform(35, 100, N)
    cooling_setpoint = rng.uniform(18, 27, N)
    humidity = rng.uniform(35, 80, N)

    compute_energy = (
        350
        + 8.0 * server_utilization
        + 5.5 * workload_intensity
        + 0.035 * server_utilization ** 2
    )

    thermal_load = (
        0.45 * np.maximum(ambient_temperature - 20, 0)
        + 0.30 * cooling_intensity
        + 0.8 * np.maximum(24 - cooling_setpoint, 0)
    )

    energy = (
        compute_energy
        + 4.5 * thermal_load
        + 0.025 * cooling_intensity ** 2
        + rng.normal(0, 10, N)
    )
    energy = np.maximum(energy, 0)

    water = (
        500
        + 10.5 * thermal_load
        + 0.018 * energy
        + 1.8 * np.maximum(ambient_temperature - 28, 0) ** 2
        + rng.normal(0, 15, N)
    )
    water = np.maximum(water, 0)

    carbon = (
        0.38 * energy
        + 0.0015 * water
        + rng.normal(0, 4, N)
    )
    carbon = np.maximum(carbon, 0)

    required_cooling = (
        0.75 * workload_intensity
        + 0.50 * np.maximum(ambient_temperature - 25, 0)
        + 0.15 * server_utilization
    )
    cooling_deficit = np.maximum(required_cooling - cooling_intensity, 0)
    thermal_stress = np.maximum(ambient_temperature - 30, 0)

    performance = (
        100
        - 0.80 * cooling_deficit
        - 0.50 * thermal_stress
        - 0.035 * np.maximum(server_utilization - 92, 0) ** 2
        - 0.025 * np.maximum(workload_intensity - 94, 0) ** 2
        - 0.05 * np.maximum(humidity - 70, 0)
        + rng.normal(0, 0.20, N)
    )
    performance = np.clip(performance, 60, 100)

    data = pd.DataFrame({
        "Server_Utilization": server_utilization,
        "Workload_Intensity": workload_intensity,
        "Ambient_Temperature": ambient_temperature,
        "Cooling_Intensity": cooling_intensity,
        "Cooling_Setpoint": cooling_setpoint,
        "Humidity": humidity,
        "Energy_kWh": energy,
        "Water_Litres": water,
        "Carbon_kg": carbon,
        "Performance_Score": performance,
    })
    return data


# ---------------------------------------------------------------------
# 2. TRAIN THE 4 RANDOM FOREST MODELS (exact params from your Colab)
# ---------------------------------------------------------------------
@st.cache_resource
def train_models():
    data = generate_synthetic_data()
    X = data[FEATURES]

    X_train, X_test, y_train_all, y_test_all = train_test_split(
        X, data[TARGETS], test_size=0.20, random_state=42
    )

    models, metrics = {}, {}
    for target in TARGETS:
        model = RandomForestRegressor(
            n_estimators=220, max_depth=18, min_samples_leaf=2,
            random_state=42, n_jobs=-1
        )
        model.fit(X_train, y_train_all[target])
        prediction = model.predict(X_test)
        metrics[target] = {
            "MAE": mean_absolute_error(y_test_all[target], prediction),
            "R2": r2_score(y_test_all[target], prediction),
        }
        models[target] = model

    explainer = shap.TreeExplainer(models["Energy_kWh"])
    return models, metrics, explainer


MODELS, METRICS, EXPLAINER = train_models()


def predict_all(config: dict):
    row = pd.DataFrame([config])[FEATURES]
    return {t: float(MODELS[t].predict(row)[0]) for t in TARGETS}


def shap_for_config(config: dict):
    row = pd.DataFrame([config])[FEATURES]
    shap_values = EXPLAINER.shap_values(row)
    return dict(zip(FEATURES, shap_values[0]))


# ---------------------------------------------------------------------
# 3. SCENARIO GENERATION (exact logic from your Colab, parameterized
#    around whatever "current state" the user has set on the sliders)
# ---------------------------------------------------------------------
def generate_scenarios(current_state, n, rng):
    su0 = current_state["Server_Utilization"]
    wl0 = current_state["Workload_Intensity"]
    at0 = current_state["Ambient_Temperature"]
    hu0 = current_state["Humidity"]

    rows = []
    for _ in range(n):
        server_value = np.clip(su0 + rng.normal(0, 3.5), su0 - 6, su0 + 8)
        workload_value = np.clip(wl0 + rng.normal(0, 3.5), wl0 - 7, wl0 + 7)
        temperature_value = np.clip(at0 + rng.normal(0, 1.5), at0 - 3, at0 + 2)
        humidity_value = np.clip(hu0 + rng.normal(0, 3), hu0 - 12, hu0 + 8)

        approximate_required_cooling = (
            0.75 * workload_value
            + 0.50 * max(temperature_value - 25, 0)
            + 0.15 * server_value
        )
        cooling_value = np.clip(
            approximate_required_cooling + rng.uniform(0, 18), 60, 100
        )
        setpoint_value = rng.uniform(20, 24)

        rows.append({
            "Server_Utilization": server_value,
            "Workload_Intensity": workload_value,
            "Ambient_Temperature": temperature_value,
            "Cooling_Intensity": cooling_value,
            "Cooling_Setpoint": setpoint_value,
            "Humidity": humidity_value,
        })
    return pd.DataFrame(rows)


def calculate_pareto_front(values, chunk_size=250):
    n = len(values)
    efficient = np.ones(n, dtype=bool)

    for start in range(0, n, chunk_size):
        end = min(start + chunk_size, n)
        chunk = values[start:end]

        no_worse = values[None, :, :] <= chunk[:, None, :]
        strictly_better = values[None, :, :] < chunk[:, None, :]
        dominates = no_worse.all(axis=2) & strictly_better.any(axis=2)

        for local_i in range(end - start):
            global_i = start + local_i
            dominates[local_i, global_i] = False

        efficient[start:end] = ~dominates.any(axis=1)

    return efficient


def run_optimization(current_state, n_candidates=3000, seed=None):
    rng = np.random.RandomState(seed if seed is not None else np.random.randint(0, 999999))

    scenarios = generate_scenarios(current_state, n_candidates, rng)
    for target in TARGETS:
        scenarios[target] = MODELS[target].predict(scenarios[FEATURES])

    feasible = scenarios[scenarios["Performance_Score"] >= MIN_PERFORMANCE].copy()

    # Safety fallback: expand search if too few feasible configs
    if len(feasible) < 20:
        extra = generate_scenarios(current_state, 2000, rng)
        for target in TARGETS:
            extra[target] = MODELS[target].predict(extra[FEATURES])
        scenarios = pd.concat([scenarios, extra], ignore_index=True)
        feasible = scenarios[scenarios["Performance_Score"] >= MIN_PERFORMANCE].copy()

    fallback_used = False
    if len(feasible) == 0:
        feasible = scenarios.nlargest(100, "Performance_Score").copy()
        fallback_used = True

    objective_columns = ["Energy_kWh", "Water_Litres", "Carbon_kg"]
    objective_values = feasible[objective_columns].values
    pareto_mask = calculate_pareto_front(objective_values)
    pareto = feasible[pareto_mask].copy()

    for column in objective_columns:
        lo, hi = pareto[column].min(), pareto[column].max()
        pareto[column + "_norm"] = 0 if hi == lo else (pareto[column] - lo) / (hi - lo)

    p_lo, p_hi = pareto["Performance_Score"].min(), pareto["Performance_Score"].max()
    pareto["Performance_norm"] = 1 if p_hi == p_lo else (pareto["Performance_Score"] - p_lo) / (p_hi - p_lo)

    pareto["Decision_Score"] = (
        0.30 * (1 - pareto["Energy_kWh_norm"])
        + 0.25 * (1 - pareto["Water_Litres_norm"])
        + 0.25 * (1 - pareto["Carbon_kg_norm"])
        + 0.20 * pareto["Performance_norm"]
    )
    pareto = pareto.sort_values("Decision_Score", ascending=False)

    return {
        "n_evaluated": len(scenarios),
        "n_feasible": len(feasible),
        "n_pareto": len(pareto),
        "fallback_used": fallback_used,
        "pareto": pareto,
        "recommended": pareto.iloc[0].to_dict() if len(pareto) > 0 else None,
    }


# ---------------------------------------------------------------------
# 4. UI
# ---------------------------------------------------------------------
if "config" not in st.session_state:
    st.session_state.config = DEFAULT_STATE.copy()
if "opt_result" not in st.session_state:
    st.session_state.opt_result = None

st.title("🌱 EcoOptiX")
st.subheader("Explainable AI for Data-Centre Sustainability Optimization")
st.write(
    "An AI-powered decision engine that evaluates what-if operating strategies "
    "and identifies sustainable data-centre configurations while maintaining performance."
)
st.divider()

# ---- CURRENT DATA CENTRE ----
st.header("1️⃣ Current Data-Centre State")
c1, c2, c3 = st.columns(3)
with c1:
    st.session_state.config["Server_Utilization"] = st.slider(
        SLIDER_LABELS["Server_Utilization"], 20.0, 100.0, st.session_state.config["Server_Utilization"])
    st.session_state.config["Workload_Intensity"] = st.slider(
        SLIDER_LABELS["Workload_Intensity"], 20.0, 100.0, st.session_state.config["Workload_Intensity"])
with c2:
    st.session_state.config["Ambient_Temperature"] = st.slider(
        SLIDER_LABELS["Ambient_Temperature"], 18.0, 42.0, st.session_state.config["Ambient_Temperature"])
    st.session_state.config["Cooling_Intensity"] = st.slider(
        SLIDER_LABELS["Cooling_Intensity"], 35.0, 100.0, st.session_state.config["Cooling_Intensity"])
with c3:
    st.session_state.config["Cooling_Setpoint"] = st.slider(
        SLIDER_LABELS["Cooling_Setpoint"], 18.0, 27.0, st.session_state.config["Cooling_Setpoint"])
    st.session_state.config["Humidity"] = st.slider(
        SLIDER_LABELS["Humidity"], 35.0, 80.0, st.session_state.config["Humidity"])

current_config = st.session_state.config
current_preds = predict_all(current_config)

st.divider()

# ---- CURRENT IMPACT ----
st.header("2️⃣ Current Predicted Impact")
k1, k2, k3, k4 = st.columns(4)
k1.metric("⚡ Energy", f"{current_preds['Energy_kWh']:.2f} kWh")
k2.metric("💧 Water", f"{current_preds['Water_Litres']:.2f} L")
k3.metric("🌫️ Carbon", f"{current_preds['Carbon_kg']:.2f} kg")
k4.metric("🚀 Performance", f"{current_preds['Performance_Score']:.2f}")

with st.expander("Model validation metrics (on held-out test data)"):
    mcols = st.columns(4)
    for i, t in enumerate(TARGETS):
        mcols[i].write(f"**{t}**  \nMAE: {METRICS[t]['MAE']:.3f}  \nR²: {METRICS[t]['R2']:.4f}")

st.divider()

# ---- SHAP ----
st.header("3️⃣ AI Explanation — Why is Energy High?")
st.write("The model identifies which operating factors contribute most to the predicted energy consumption.")

shap_vals = shap_for_config(current_config)
shap_df = pd.DataFrame({
    "Feature": FEATURES,
    "SHAP Value": [shap_vals[f] for f in FEATURES],
}).sort_values("SHAP Value", key=abs, ascending=True)

fig_shap = px.bar(
    shap_df, x="SHAP Value", y="Feature", orientation="h",
    color="SHAP Value", color_continuous_scale="RdYlGn_r",
    title="SHAP Feature Contribution to Energy Prediction"
)
st.plotly_chart(fig_shap, use_container_width=True)

st.divider()

# ---- WHAT-IF SIMULATOR ----
st.header("4️⃣ What-If Simulator")
st.write("Modify operating conditions below and compare against the current baseline.")

wc1, wc2, wc3 = st.columns(3)
whatif = {}
with wc1:
    whatif["Server_Utilization"] = st.slider(
        "What-if: Server Utilization", 20.0, 100.0, current_config["Server_Utilization"], key="wi_su")
    whatif["Workload_Intensity"] = st.slider(
        "What-if: Workload Intensity", 20.0, 100.0, current_config["Workload_Intensity"], key="wi_wl")
with wc2:
    whatif["Ambient_Temperature"] = st.slider(
        "What-if: Ambient Temperature", 18.0, 42.0, current_config["Ambient_Temperature"], key="wi_at")
    whatif["Cooling_Intensity"] = st.slider(
        "What-if: Cooling Intensity", 35.0, 100.0, current_config["Cooling_Intensity"], key="wi_ci")
with wc3:
    whatif["Cooling_Setpoint"] = st.slider(
        "What-if: Cooling Setpoint", 18.0, 27.0, current_config["Cooling_Setpoint"], key="wi_cs")
    whatif["Humidity"] = st.slider(
        "What-if: Humidity", 35.0, 80.0, current_config["Humidity"], key="wi_hu")

whatif_preds = predict_all(whatif)

wcols = st.columns(4)
pairs = [("Energy (kWh)", "Energy_kWh"), ("Water (L)", "Water_Litres"),
         ("Carbon (kg)", "Carbon_kg"), ("Performance", "Performance_Score")]
for col, (label, key) in zip(wcols, pairs):
    delta = whatif_preds[key] - current_preds[key]
    col.metric(label, f"{whatif_preds[key]:.2f}", delta=f"{delta:+.2f}",
               delta_color="inverse" if key != "Performance_Score" else "normal")

st.divider()

# ---- OPTIMIZATION ENGINE ----
st.header("5️⃣ Optimization Engine")
st.write(
    f"Click below to generate candidate operating configurations near the current state, "
    f"filter for feasible ones (Performance ≥ {MIN_PERFORMANCE:.0f}), find Pareto-optimal "
    f"trade-offs, and select the best-balanced configuration."
)
st.caption("Decision weights → Energy: 30%, Water: 25%, Carbon: 25%, Performance: 20%")

if st.button("🔍 Optimize Sustainability", type="primary"):
    with st.spinner("Evaluating configurations..."):
        st.session_state.opt_result = run_optimization(current_config, n_candidates=3000, seed=42)

result = st.session_state.opt_result

if result:
    oc1, oc2, oc3 = st.columns(3)
    oc1.metric("Configurations Evaluated", result["n_evaluated"])
    oc2.metric(f"Feasible (Performance ≥ {MIN_PERFORMANCE:.0f})", result["n_feasible"])
    oc3.metric("Pareto-Optimal Found", result["n_pareto"])
    if result["fallback_used"]:
        st.info("No configuration met the performance constraint — showing top-performance configurations instead.")

    rec = result["recommended"]
    if rec is None:
        st.warning("No configurations could be evaluated.")
    else:
        st.divider()
        st.header("6️⃣ Recommended Strategy")

        comp_rows = [{"Parameter": f, "Current": round(current_config[f], 2), "Recommended": round(rec[f], 2)}
                     for f in FEATURES]
        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)

        st.subheader("Predicted Impact — Recommended Configuration")
        rcols = st.columns(4)
        rcols[0].metric("⚡ Energy", f"{rec['Energy_kWh']:.2f} kWh",
                         delta=f"{rec['Energy_kWh']-current_preds['Energy_kWh']:+.2f}", delta_color="inverse")
        rcols[1].metric("💧 Water", f"{rec['Water_Litres']:.2f} L",
                         delta=f"{rec['Water_Litres']-current_preds['Water_Litres']:+.2f}", delta_color="inverse")
        rcols[2].metric("🌫️ Carbon", f"{rec['Carbon_kg']:.2f} kg",
                         delta=f"{rec['Carbon_kg']-current_preds['Carbon_kg']:+.2f}", delta_color="inverse")
        rcols[3].metric("🚀 Performance", f"{rec['Performance_Score']:.2f}",
                         delta=f"{rec['Performance_Score']-current_preds['Performance_Score']:+.2f}")
        st.caption(f"Decision Score: **{rec['Decision_Score']:.4f}**")

        st.divider()

        st.header("7️⃣ Impact Visualization — Current vs Recommended")
        vc1, vc2 = st.columns(2)
        with vc1:
            fig_bar = go.Figure(data=[
                go.Bar(name="Current", x=["Energy", "Water", "Carbon"],
                       y=[current_preds["Energy_kWh"], current_preds["Water_Litres"], current_preds["Carbon_kg"]]),
                go.Bar(name="Recommended", x=["Energy", "Water", "Carbon"],
                       y=[rec["Energy_kWh"], rec["Water_Litres"], rec["Carbon_kg"]]),
            ])
            fig_bar.update_layout(barmode="group", title="Resource Consumption")
            st.plotly_chart(fig_bar, use_container_width=True)
        with vc2:
            fig_perf = go.Figure(data=[
                go.Bar(name="Current", x=["Performance"], y=[current_preds["Performance_Score"]]),
                go.Bar(name="Recommended", x=["Performance"], y=[rec["Performance_Score"]]),
            ])
            fig_perf.update_layout(barmode="group", title="Performance", yaxis_range=[0, 100])
            st.plotly_chart(fig_perf, use_container_width=True)

        def pct(cur, new):
            return (cur - new) / cur * 100 if cur != 0 else 0.0

        pcols = st.columns(4)
        pcols[0].metric("Energy Reduction", f"{pct(current_preds['Energy_kWh'], rec['Energy_kWh']):.2f}%")
        pcols[1].metric("Water Reduction", f"{pct(current_preds['Water_Litres'], rec['Water_Litres']):.2f}%")
        pcols[2].metric("Carbon Reduction", f"{pct(current_preds['Carbon_kg'], rec['Carbon_kg']):.2f}%")
        pcols[3].metric("Performance Change", f"{rec['Performance_Score']-current_preds['Performance_Score']:+.2f} pts")

        st.divider()

        st.header("8️⃣ Pareto Front — Trade-off Configurations")
        st.write(
            "These configurations represent different trade-offs between sustainability objectives. "
            "The selected configuration provides the best balance according to the chosen decision weights."
        )
        pareto_df = result["pareto"]
        fig_pareto = px.scatter(
            pareto_df, x="Energy_kWh", y="Water_Litres", size="Performance_Score", color="Carbon_kg",
            hover_data=["Cooling_Intensity", "Cooling_Setpoint", "Performance_Score", "Decision_Score"],
            color_continuous_scale="Viridis",
            title="Pareto-Optimal Sustainability Strategies"
        )
        fig_pareto.add_scatter(
            x=[rec["Energy_kWh"]], y=[rec["Water_Litres"]], mode="markers",
            marker=dict(size=18, color="red", symbol="star"), name="Recommended"
        )
        st.plotly_chart(fig_pareto, use_container_width=True)

        with st.expander("View top 10 Pareto-optimal configurations"):
            show_cols = FEATURES + TARGETS + ["Decision_Score"]
            st.dataframe(pareto_df[show_cols].head(10).round(2), use_container_width=True, hide_index=True)

st.divider()

st.warning(
    "⚠️ **Disclaimer:** Prototype uses synthetic telemetry for demonstration. "
    "Results are model predictions and should be calibrated with real data before operational deployment."
)

with st.expander("☁️ Planned Cloud Architecture"):
    st.markdown("""
**Deployment plan:**

```
User
 ↓
Streamlit Application
 ↓
AWS EC2  →  ML + SHAP + Optimization Engine  →  Recommendation
 ↑
AWS S3  →  Telemetry / Model Artifacts
```

The Streamlit app runs on an EC2 instance. Trained models and telemetry snapshots
are stored in S3 for persistence and versioning, allowing the app to be redeployed
or retrained without re-uploading data manually.
""")
