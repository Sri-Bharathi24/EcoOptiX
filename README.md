# EcoOptiX
Explainable AI for Data-Centre Sustainability Optimization

# 🌱 EcoOptiX

### Explainable AI for Data-Centre Sustainability Optimization

> **Predict. Explain. Simulate. Optimize. Recommend.**

EcoOptiX is an **Explainable AI-powered decision-support engine** designed to help data centres identify more sustainable operating configurations.

Instead of simply monitoring energy, water, carbon, and performance, EcoOptiX answers a more useful question:

> **"What operating configuration should the data centre use to achieve a better sustainability–performance balance?"**

The system combines **Machine Learning, Explainable AI, What-If Simulation, Multi-Objective Optimization, and Pareto Analysis** to generate actionable recommendations.

---

## 🧩 Problem

Modern data centres consume significant amounts of:

* ⚡ Energy
* 💧 Water
* 🌍 Carbon resources
* 🖥️ Computing capacity

Traditional monitoring systems mainly show **what is happening**.

Some systems may also identify **why consumption is high**.

However, they often do not answer:

> **"What should we change to improve sustainability without sacrificing performance?"**

EcoOptiX bridges this gap by transforming telemetry data into **explainable and optimized operating recommendations**.

---

# 💡 Solution

EcoOptiX follows a complete decision-support pipeline:

```text
Current Data-Centre State
          ↓
   ML Prediction
  (Random Forest × 4)
          ↓
   SHAP Explainability
          ↓
   What-If Simulation
          ↓
 Performance Constraint
      (≥ 96)
          ↓
 Multi-Objective Optimization
          ↓
     Pareto Front
          ↓
    Decision Scoring
          ↓
 Recommended Configuration
```

The system predicts four important outcomes:

| Target          | Description                           |
| --------------- | ------------------------------------- |
| ⚡ Energy        | Predicted energy consumption in kWh   |
| 💧 Water        | Predicted water consumption in litres |
| 🌍 Carbon       | Predicted carbon emissions in kg      |
| 🖥️ Performance | Predicted system performance score    |

---

# ⚙️ How EcoOptiX Works

## 1. 🤖 ML Prediction

EcoOptiX uses **four Random Forest regression models** to predict:

* Energy consumption
* Water consumption
* Carbon emissions
* Performance

The models use six operating parameters:

1. Server utilization
2. Workload intensity
3. Ambient temperature
4. Cooling intensity
5. Cooling setpoint
6. Humidity

Each model independently predicts one sustainability or performance metric.

---

## 2. 🔍 SHAP Explainability

Machine-learning predictions are not enough.

EcoOptiX uses **SHAP (SHapley Additive exPlanations)** to explain the prediction.

For example:

```text
Why is energy consumption high?

Server Utilization      ████████████
Cooling Intensity       █████████
Ambient Temperature     ██████
Workload Intensity      █████
Humidity                ███
Cooling Setpoint        ██
```

This helps the user understand:

> **Which operating factors are contributing most to the predicted energy consumption?**

Instead of treating the ML model as a black box, EcoOptiX provides an interpretable explanation.

---

# 🔄 3. What-If Simulation

Users can modify operating parameters and immediately evaluate the predicted impact.

For example:

```text
Current Configuration
Server Utilization: 82%
Cooling Intensity: 75%
Temperature: 30°C

            ↓ Change

Scenario Configuration
Server Utilization: 78%
Cooling Intensity: 68%
Temperature: 28°C

            ↓

EcoOptiX predicts:

Energy     ↓
Water      ↓
Carbon     ↓
Performance → Maintained
```

This allows users to explore possible operating strategies before selecting one.

---

# 🎯 4. Multi-Objective Optimization

EcoOptiX generates multiple candidate configurations around the current operating state.

Each candidate is evaluated using the four ML models.

Configurations that fail the minimum performance requirement are removed.

### Performance Constraint

```text
Performance ≥ 96
```

The remaining configurations are evaluated across:

* Energy
* Water
* Carbon

Because improving one objective may negatively affect another, EcoOptiX uses **Pareto optimization** to identify non-dominated solutions.

---

# 📈 5. Pareto Front

The Pareto front represents the trade-offs between sustainability objectives.

For example:

```text
             Carbon
               ↑
               │       ●
               │    ●
               │  ●
               │ ●
               │________________→ Energy
```

A configuration may have:

* Lower energy but higher water consumption
* Lower carbon but slightly higher energy
* Lower water consumption but reduced performance

EcoOptiX exposes these trade-offs instead of hiding them behind a single metric.

---

# ⚖️ 6. Decision Scoring

After identifying Pareto-optimal configurations, EcoOptiX ranks them using a weighted decision score.

### Current Weights

| Objective       | Weight |
| --------------- | -----: |
| ⚡ Energy        |    30% |
| 💧 Water        |    25% |
| 🌍 Carbon       |    25% |
| 🖥️ Performance |    20% |

```text
Decision Score =
    Energy       × 30%
  + Water        × 25%
  + Carbon       × 25%
  + Performance  × 20%
```

The highest-ranked balanced configuration becomes the final recommendation.

> The weights can be adjusted depending on the priorities of a specific data-centre operator.

---

# 🚀 Key Features

### 📊 Sustainability Prediction

Predicts:

* Energy consumption
* Water consumption
* Carbon emissions
* Performance

### 🔍 Explainable AI

Uses SHAP to identify the factors influencing predictions.

### 🎛️ What-If Simulator

Allows users to experiment with different operating configurations.

### 🧠 Intelligent Optimization

Searches for better configurations instead of simply reporting current consumption.

### 📈 Pareto Analysis

Shows trade-offs between energy, water, and carbon.

### 🏆 Decision Recommendation

Selects a balanced configuration based on configurable priorities.

### 📉 Impact Comparison

Compares the current configuration against the recommended configuration.

---

# 📊 Model Validation

The models were evaluated on **held-out test data**.

| Target          |   MAE |     R² |
| --------------- | ----: | -----: |
| ⚡ Energy (kWh)  | 20.60 | 0.9936 |
| 💧 Water (L)    | 14.22 | 0.9859 |
| 🌍 Carbon (kg)  |  8.56 | 0.9924 |
| 🖥️ Performance |  0.69 | 0.9804 |

The results demonstrate strong predictive performance on the synthetic dataset used for this prototype.

> **Important:** These metrics represent performance on simulated data and should not be interpreted as production-grade accuracy.

---

# 🏗️ System Architecture

## Local Architecture

```text
                ┌──────────────────────┐
                │       User           │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Streamlit Application│
                └──────────┬───────────┘
                           ↓
             ┌────────────────────────────┐
             │      ML Prediction         │
             │   Random Forest × 4        │
             └─────────────┬──────────────┘
                           ↓
             ┌────────────────────────────┐
             │      SHAP Explainability   │
             └─────────────┬──────────────┘
                           ↓
             ┌────────────────────────────┐
             │     What-If Simulation     │
             └─────────────┬──────────────┘
                           ↓
             ┌────────────────────────────┐
             │ Multi-Objective Optimizer   │
             └─────────────┬──────────────┘
                           ↓
             ┌────────────────────────────┐
             │   Recommendation Engine    │
             └────────────────────────────┘
```

---

# ☁️ Planned AWS Architecture

EcoOptiX is designed to be deployable on AWS.

```text
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 ↓
                     ┌─────────────────────┐
                     │ Streamlit Application│
                     └──────────┬──────────┘
                                ↓
                     ┌─────────────────────┐
                     │      AWS EC2        │
                     │                     │
                     │ ML Prediction       │
                     │ SHAP                │
                     │ Optimization        │
                     │ Recommendation      │
                     └──────────┬──────────┘
                                ↑
                                │
                     ┌──────────┴──────────┐
                     │      AWS S3         │
                     │                     │
                     │ Model Artifacts     │
                     │ Telemetry Snapshots │
                     │ Model Versions      │
                     └─────────────────────┘
```

### AWS Components

**Amazon EC2**

Hosts the Streamlit application and inference/optimization engine.

**Amazon S3**

Stores:

* Trained ML models
* Model artifacts
* Telemetry snapshots
* Versioned deployment files

This architecture allows models and telemetry artifacts to be updated without manually rebuilding the entire application.

---

# 🛠️ Technology Stack

| Technology      | Purpose                     |
| --------------- | ---------------------------- |
| 🐍 Python       | Core development            |
| 🎨 Streamlit    | Web application and UI      |
| 🤖 Scikit-learn | Random Forest ML models     |
| 🔍 SHAP         | Explainable AI              |
| 📊 Plotly       | Interactive visualizations  |
| 🐼 Pandas       | Data processing             |
| 🔢 NumPy        | Numerical computation       |
| ☁️ AWS EC2      | Application hosting (planned) |
| 🪣 AWS S3       | Model and telemetry storage (planned) |

---

# 📁 Project Structure

```text
ecooptix/
│
├── app.py              # Full application — data generation, ML models,
│                        # SHAP, optimization engine, and Streamlit UI
├── requirements.txt    # Python dependencies
└── README.md
```

> EcoOptiX is intentionally kept as a single-file application for this hackathon
> prototype. Synthetic telemetry is generated in-memory and the four Random
> Forest models are trained at app startup (cached), so no external model or
> data files are required to run it. AWS EC2/S3 integration described above is
> the planned next step for production deployment, not part of the current
> prototype.

---

# ▶️ Run Locally

## 1. Clone the repository

```bash
git clone https://github.com/Sri-Bharathi24/EcoOptiX.git
cd EcoOptiX
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the application

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

---

# 📦 Requirements

```text
streamlit
pandas
numpy
scikit-learn
shap
plotly
```

---

# 🧪 Example Workflow

### Step 1 — Enter Current State

```text
Server Utilization    → 82%
Workload Intensity    → 85%
Ambient Temperature   → 36°C
Cooling Intensity     → 78%
Cooling Setpoint      → 21°C
Humidity              → 62%
```

### Step 2 — Predict

EcoOptiX generates:

```text
Energy       → Predicted value
Water        → Predicted value
Carbon       → Predicted value
Performance  → Predicted value
```

### Step 3 — Explain

SHAP identifies the most influential parameters.

### Step 4 — Explore

The user changes parameters using the What-If simulator.

### Step 5 — Optimize

EcoOptiX searches candidate configurations while enforcing:

```text
Performance ≥ 96
```

### Step 6 — Recommend

The system returns:

```text
Recommended Configuration

✓ Improved sustainability
✓ Performance constraint satisfied
✓ Balanced Energy / Water / Carbon
✓ Explainable decision
```

---

# 🌍 Why EcoOptiX?

Traditional monitoring:

```text
"What is happening?"
```

Analytics:

```text
"Why is it happening?"
```

EcoOptiX:

```text
"What should we do next?"
```

This transforms sustainability monitoring into **AI-assisted operational decision support**.

---

# 🔬 Innovation

EcoOptiX combines multiple AI techniques into a single decision pipeline:

```text
Machine Learning
       +
Explainable AI
       +
What-If Simulation
       +
Multi-Objective Optimization
       +
Pareto Analysis
       +
Decision Scoring
       =
Actionable Sustainability Recommendation
```

The goal is not simply to predict resource consumption.

The goal is to identify **better operating strategies while maintaining performance**.

---

# ⚠️ Disclaimer

EcoOptiX is a **prototype developed for demonstration and hackathon purposes**.

The current implementation uses **synthetic data/telemetry**.

Therefore:

* Predictions are based on simulated data.
* Savings percentages are model outputs.
* Recommendations are not intended for direct production deployment.
* Real-world deployment would require calibration and validation using actual data-centre telemetry.
* Operational decisions should be validated against safety, reliability, workload, and infrastructure constraints.

---

# 🚀 Future Scope

Potential future improvements include:

* 🔴 Real-time data-centre telemetry integration
* 📡 IoT sensor integration
* ☁️ Automated AWS telemetry pipelines
* 🧠 Advanced optimization algorithms
* 📈 Historical sustainability analytics
* 🔄 Continuous model retraining
* 🏢 Multi-data-centre optimization
* 💰 Cost-aware optimization
* 🌦️ Weather-aware cooling optimization
* 👥 Role-based dashboards
* 🔐 Secure enterprise deployment
* 📊 Carbon-intensity-aware optimization
* 🤖 Automated operational recommendations

---

# 🎬 Demo

EcoOptiX can be demonstrated through a simple end-to-end workflow.

### 1. Enter the Current Data-Centre State

The user provides the current operating conditions, e.g.:

```text
Server Utilization    → 82%
Workload Intensity    → 75%
Ambient Temperature   → 30°C
Cooling Intensity     → 70%
Cooling Setpoint      → 24°C
Humidity              → 55%
```

### 2. Predict Sustainability Metrics

EcoOptiX uses four Random Forest models to predict:

```text
⚡ Energy Consumption
💧 Water Consumption
🌍 Carbon Emissions
🖥️ Performance
```

The dashboard displays the predicted values immediately.

### 3. Understand the Prediction

The SHAP explainability module identifies the operating parameters that have the greatest influence on the energy prediction.

The user can therefore understand:

```text
WHY is energy consumption high?
```

rather than receiving only a prediction.

### 4. Run a What-If Scenario

The user can modify operating parameters using the Streamlit controls.

For example:

```text
Current
Cooling Intensity → 70%

What-If
Cooling Intensity → 65%
```

EcoOptiX recalculates the expected:

* Energy
* Water
* Carbon
* Performance

This allows different strategies to be explored before optimization.

### 5. Run Optimization

The optimization engine generates candidate configurations around the current state.

Configurations that do not satisfy:

```text
Performance ≥ 96
```

are filtered out.

The remaining configurations are evaluated across:

```text
Energy + Water + Carbon
```

and the Pareto-optimal configurations are identified.

### 6. View the Pareto Front

The dashboard displays the sustainability trade-offs between candidate configurations.

This helps the user understand that there is not always a single configuration that minimizes every objective simultaneously.

### 7. Receive the Final Recommendation

EcoOptiX applies the configured decision weights:

```text
Energy       → 30%
Water        → 25%
Carbon       → 25%
Performance  → 20%
```

The system selects the best-balanced configuration and displays:

```text
✓ Recommended operating configuration
✓ Predicted energy impact
✓ Predicted water impact
✓ Predicted carbon impact
✓ Performance score
✓ Improvement compared with current state
```

### 🎯 Complete Demo Flow

```text
Current State
      ↓
Predict
      ↓
Explain with SHAP
      ↓
Change Parameters
      ↓
What-If Prediction
      ↓
Optimize
      ↓
Pareto Front
      ↓
Decision Score
      ↓
Recommended Configuration
```

> **Demo goal:** Show that EcoOptiX does not stop at prediction. It converts predictions into an explainable, constraint-aware operating recommendation.

---

# ☁️ Deployment

The current hackathon submission runs as a **Streamlit Community Cloud** app directly from this GitHub repository — no server setup required to try it.

EcoOptiX is additionally designed to be deployable on **Amazon Web Services (AWS)** using an EC2 instance for application hosting and Amazon S3 for model and telemetry storage, as a next step beyond the hackathon prototype.

## Planned AWS Architecture

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ↓
                         ┌──────────────────┐
                         │    Streamlit     │
                         │   Web Interface  │
                         └────────┬─────────┘
                                  │
                                  ↓
                    ┌─────────────────────────┐
                    │       AWS EC2           │
                    │                         │
                    │  ML Prediction          │
                    │  SHAP Explainability    │
                    │  What-If Simulation     │
                    │  Optimization Engine    │
                    │  Recommendation Engine  │
                    └────────────┬────────────┘
                                 │
                                 ↓
                    ┌─────────────────────────┐
                    │        AWS S3            │
                    │                         │
                    │  ML Models              │
                    │  Model Versions         │
                    │  Telemetry Snapshots    │
                    │  Application Artifacts  │
                    └─────────────────────────┘
```

> **Note:** In the current prototype, models are trained in-memory at
> application startup — there are no `.pkl` files or an S3 dependency yet.
> The steps below describe the planned path to a persistent AWS deployment.

---

## 🚀 Deploy on AWS EC2 (Planned)

### Step 1 — Launch an EC2 Instance

Create an EC2 instance using a Linux-based AMI.

Configure the security group to allow:

```text
SSH   → Port 22
HTTP  → Port 80
Custom TCP → Port 8501
```

Port `8501` is used by Streamlit by default.

### Step 2 — Connect to EC2

```bash
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP
```

The exact username depends on the AMI being used.

### Step 3 — Install Required Packages

```bash
sudo yum update -y
sudo yum install git python3 -y
```

For Ubuntu-based instances:

```bash
sudo apt update
sudo apt install git python3 python3-pip -y
```

### Step 4 — Clone EcoOptiX

```bash
git clone https://github.com/Sri-Bharathi24/EcoOptiX.git
cd EcoOptiX
```

### Step 5 — Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 6 — Run Streamlit

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

The application can then be accessed through:

```text
http://YOUR_EC2_PUBLIC_IP:8501
```

---

## 🪣 AWS S3 Integration (Planned)

Once the ML models are exported (e.g. via `joblib`) instead of trained in-memory, S3 could be used to store and version EcoOptiX artifacts:

```text
ecooptix-s3/
│
├── models/
│   ├── energy_model.pkl
│   ├── water_model.pkl
│   ├── carbon_model.pkl
│   └── performance_model.pkl
│
├── telemetry/
│   └── telemetry_snapshots/
│
└── versions/
    ├── model-v1/
    └── model-v2/
```

This would allow the application to retrieve trained models and telemetry artifacts without keeping every version directly inside the EC2 deployment.

---

## 🔄 Deployment Workflow (Planned)

```text
Developer
    ↓
GitHub Repository
    ↓
AWS EC2
    ↓
EcoOptiX Streamlit Application
    ↓
Load ML Models / Telemetry
    ↑
AWS S3
```

### Model Update Workflow

```text
New Model
    ↓
Upload to S3
    ↓
Create New Model Version
    ↓
EC2 Retrieves Model
    ↓
EcoOptiX Uses Updated Model
```

This provides a foundation for future **model versioning and continuous deployment**.

---

# 🔐 Production Considerations

The hackathon deployment is intended as a prototype. A production deployment would additionally require:

* HTTPS
* Authentication and authorization
* Restricted security-group rules
* IAM roles instead of hard-coded credentials
* S3 bucket security policies
* Application monitoring
* Model version management
* Logging and audit trails
* Automated backups
* Real-time telemetry pipelines
* Validation against real data-centre infrastructure

> **Important:** EcoOptiX recommendations should not directly control production cooling or infrastructure equipment without extensive validation, safety constraints, and human approval.

---

# 🏆 Hackathon Vision

EcoOptiX aims to demonstrate how **Explainable AI can move beyond prediction and monitoring toward actionable sustainability decisions**.

> ### **"Don't just monitor the data centre. Optimize what it does next."**

---

# 👤 Author

**Sri Bharathi VN**
Built individually for a 6-day hackathon submission.

### 🌱 EcoOptiX

**Explainable AI for Data-Centre Sustainability Optimization**
