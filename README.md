# SnapShield AI

**Private On-Device Scam & Phishing Detector**

SnapShield AI is a local-first desktop prototype that analyzes suspicious messages and URLs and returns an understandable risk level with the signals behind it.

## Core idea

**Paste → Analyze locally → Understand the risk → Decide**

The prototype combines:

- TF-IDF text features
- Logistic Regression classification
- Transparent URL checks
- Sensitive-information checks for OTP/PIN/CVV/password requests
- Explainable LOW / MEDIUM / HIGH output

## Run locally

### 1. Install Python 3.10+
### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the app

```bash
python app.py
```

## Project structure

```text
SnapShield-AI/
├── app.py
├── data.csv
├── requirements.txt
├── README.md
└── docs/
    ├── ARCHITECTURE.md
    └── DEMO_SCRIPT.md
```

## Snapdragon deployment path

The current prototype is Python-based and is intended to demonstrate the product workflow. For a production Snapdragon-powered HP PC implementation, the model boundary can be exported to an interoperable format such as ONNX and then profiled/optimized on the target Windows-on-Snapdragon environment.

**Important:** this repository does not claim Snapdragon hardware benchmarks that have not been measured.

## Responsible-use note

The included dataset is demonstration data, not a production security corpus. A production security product would require representative licensed data, adversarial testing, false-positive analysis, privacy review and target-device profiling.


## Browser demo

Open `index.html` in a modern browser for a zero-install visual demo of the SnapShield workflow.

The browser demo is a presentation/demo layer. The main AI prototype is `app.py`, which uses TF-IDF + Logistic Regression and the same product concept with a local Python runtime.
