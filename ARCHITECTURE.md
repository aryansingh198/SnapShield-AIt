# SnapShield AI — Architecture

## High-level flow

```text
User
  |
  v
Desktop UI
  |
  +--> Text / URL normalization
  |
  +--> TF-IDF text representation
  |
  +--> Logistic Regression probability
  |
  +--> Deterministic security heuristics
  |
  v
Risk score + risk band + reasons
```

## Components

### 1. Interface
`app.py` contains the Tkinter desktop interface.

### 2. Local model
The text classifier uses TF-IDF features with Logistic Regression.

### 3. Security heuristics
The prototype adds deterministic checks for:
- insecure HTTP links
- raw IP addresses in URLs
- `@` in URLs
- unusually long URLs
- OTP/PIN/CVV/password requests
- urgency and account/payment language

### 4. Explainability
The UI displays the main detected signals instead of presenting only a numerical score.

## Snapdragon path

The prototype intentionally keeps the model boundary compact. A production implementation can replace the Python inference path with an ONNX representation and then profile the model on the target Snapdragon-powered HP PC.

## Validation boundary

The demonstration dataset is only for the prototype. Production validation should include:
- representative and licensed data
- adversarial examples
- false-positive / false-negative analysis
- latency and memory profiling
- privacy and security review
