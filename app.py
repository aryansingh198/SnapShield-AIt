import csv
import re
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data.csv"

with DATA_FILE.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

texts = [r["text"] for r in rows]
labels = [int(r["label"]) for r in rows]

MODEL = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
    ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced")),
])
MODEL.fit(texts, labels)

RISK_TERMS = {
    "otp": 12, "password": 12, "verify": 8, "urgent": 7,
    "blocked": 10, "suspended": 10, "prize": 9, "winner": 9,
    "claim": 6, "refund": 8, "fee": 7, "click": 5, "bank": 6,
    "card": 8, "cvv": 14, "pin": 14, "crypto": 8, "wallet": 8,
}

def analyze(text: str):
    text = text.strip()
    if not text:
        return 0, "READY", ["Paste a message or URL to begin."]

    probability = float(MODEL.predict_proba([text])[0][1])
    score = probability * 58
    lower = text.lower()
    words = set(re.findall(r"[a-zA-Z]{3,}", lower))
    hits = sorted(words & set(RISK_TERMS), key=lambda x: -RISK_TERMS[x])

    reasons = []
    if hits:
        score += min(27, sum(RISK_TERMS[x] for x in hits))
        reasons.append("Risk language: " + ", ".join(hits[:7]))

    urls = re.findall(r"(?:https?://|www\.)\S+", lower)
    for url in urls:
        if url.startswith("http://"):
            score += 8
            reasons.append("Link does not use HTTPS.")
        if "@" in url:
            score += 12
            reasons.append("URL contains an @ symbol.")
        if re.search(r"\d{1,3}(?:\.\d{1,3}){3}", url):
            score += 14
            reasons.append("URL uses a raw IP address.")
        if len(url) > 75:
            score += 8
            reasons.append("URL is unusually long.")

    if any(x in lower for x in (
        "send otp", "share otp", "card number", "cvv", "pin",
        "share password", "send password"
    )):
        score += 15
        reasons.append("Requests sensitive authentication/payment information.")

    score = min(99, round(score))
    risk = "HIGH" if score >= 70 else "MEDIUM" if score >= 40 else "LOW"

    if not reasons:
        reasons = ["No strong suspicious signal was detected by the local model and rules."]

    return score, risk, reasons


class SnapShieldApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SnapShield AI")
        self.geometry("1000x720")
        self.minsize(850, 620)
        self.configure(bg="#07191c")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Action.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(16, 10),
        )

        tk.Label(
            self, text="SNAPSHIELD AI",
            bg="#07191c", fg="#7ee28e",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=36, pady=(24, 0))

        tk.Label(
            self, text="Private On-Device Scam & Phishing Detector",
            bg="#07191c", fg="white",
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", padx=36, pady=(4, 0))

        tk.Label(
            self,
            text="Local analysis  •  Explainable results  •  Snapdragon-ready deployment path",
            bg="#07191c", fg="#9fb9bd",
            font=("Segoe UI", 11)
        ).pack(anchor="w", padx=38, pady=(4, 16))

        panel = tk.Frame(
            self, bg="#102a2e",
            highlightthickness=1, highlightbackground="#28545a"
        )
        panel.pack(fill="both", expand=True, padx=32, pady=(0, 28))

        tk.Label(
            panel, text="Paste a suspicious message, email snippet or URL",
            bg="#102a2e", fg="#dcebed",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=24, pady=(20, 7))

        self.input_box = tk.Text(
            panel, height=8, bg="#061215", fg="#edf7f7",
            insertbackground="white", relief="flat",
            font=("Segoe UI", 12), padx=14, pady=12
        )
        self.input_box.pack(fill="x", padx=24)

        actions = tk.Frame(panel, bg="#102a2e")
        actions.pack(fill="x", padx=24, pady=12)

        ttk.Button(
            actions, text="Analyze Locally",
            style="Action.TButton", command=self.run_analysis
        ).pack(side="left")

        ttk.Button(
            actions, text="Clear",
            style="Action.TButton", command=self.clear
        ).pack(side="left", padx=10)

        self.result = tk.Label(
            panel, text="READY",
            bg="#17383d", fg="#b8d9dd",
            font=("Segoe UI", 19, "bold"), pady=10
        )
        self.result.pack(fill="x", padx=24, pady=(0, 12))

        tk.Label(
            panel, text="Why?",
            bg="#102a2e", fg="#dcebed",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", padx=24)

        self.reasons = tk.Text(
            panel, height=8, bg="#061215", fg="#c9dddf",
            relief="flat", font=("Segoe UI", 11), padx=14, pady=12
        )
        self.reasons.pack(fill="both", expand=True, padx=24, pady=(6, 20))
        self.reasons.config(state="disabled")

    def run_analysis(self):
        score, risk, why = analyze(self.input_box.get("1.0", "end"))
        self.result.config(text=f"{risk}  •  {score}/99")

        self.reasons.config(state="normal")
        self.reasons.delete("1.0", "end")
        for reason in why:
            self.reasons.insert("end", "• " + reason + "\n")
        self.reasons.config(state="disabled")

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.result.config(text="READY")
        self.reasons.config(state="normal")
        self.reasons.delete("1.0", "end")
        self.reasons.config(state="disabled")


if __name__ == "__main__":
    SnapShieldApp().mainloop()
