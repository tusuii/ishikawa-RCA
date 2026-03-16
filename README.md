# Fishbone RCA Analyzer

A Streamlit app for DevOps/SRE incident post-mortems using the Ishikawa (fishbone) diagram and the 6M framework.

![Fishbone RCA Analyzer](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)

## What it does

- **Live fishbone diagram** — SVG diagram updates in real time as you add causes across 6 categories (People, Process, Tools/Technology, Environment, Measurement, Materials/Data)
- **Incident metadata** — capture title, date, severity (P1–P4), affected service, and owner
- **DevOps presets** — one-click templates for common incidents:
  - K8s Pod CrashLoopBackOff
  - Jenkins Pipeline Failure
  - ArgoCD Sync Failure
  - Database Connection Exhaustion
- **Export** — download the diagram as SVG, or export the full post-mortem report as Markdown or JSON

## Quick start

```bash
# 1. Clone the repo
git clone <repo-url>
cd ishikawa-root-cause-streamlit

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit >= 1.35` | Web app framework |
| `svgwrite >= 1.4.3` | SVG generation |
| `reportlab >= 4.0` | PDF/report generation |
| `markdown2 >= 2.4` | Markdown rendering |

## Project structure

```
.
├── app.py                  # Entry point
├── requirements.txt
├── assets/
│   └── style.css           # Dark theme styles
├── components/
│   ├── diagram.py          # SVG fishbone builder + renderer
│   ├── form.py             # Cause input form
│   ├── report.py           # Post-mortem report panel + export
│   └── sidebar.py          # Presets + summary sidebar
└── utils/
    ├── presets.py          # Built-in DevOps incident templates
    └── state.py            # Session state management, categories, colors
```

## Usage

1. **Fill in the incident details** (title, severity, affected service, effect/problem statement) in the left panel
2. **Add causes** under each of the 6M categories
3. Watch the **fishbone diagram** update live on the right
4. Use a **preset** from the sidebar to load a pre-populated incident template
5. **Export** the diagram (SVG) or the full report (Markdown / JSON)

## 6M Categories

| Category | What to capture |
|----------|----------------|
| **People** | Human factors, training gaps, staffing issues |
| **Process** | Missing runbooks, policy gaps, workflow failures |
| **Tools / Technology** | Software bugs, misconfigurations, infra issues |
| **Environment** | Network, infrastructure, external dependencies |
| **Measurement** | Missing alerts, observability gaps, SLO breaches |
| **Materials / Data** | Config files, secrets, database issues |
