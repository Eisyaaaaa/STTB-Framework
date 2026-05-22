# Sarawak Tech-Trust Barometer (STTB)

A state-of-the-art social-technical research and data analytics platform designed to measure, visualize, and analyze public trust in digital technologies and institutions across the administrative divisions of Sarawak.

Grounded in sociological Institutional Theory by **W. Richard Scott (1995)** and refined with the ethical paradigms of Islamic jurisprudence, the platform maps civic evaluations across **5 core pillars** of digital trust and **15 variables** using a comprehensive **75-item survey instrument**.

---

## Project Organization

The repository has been organized into modular layers to cleanly decouple user interface concerns from backend mathematical scoring models and persistence mechanisms:

```
STTB-Framework/
├── README.md                 # Project documentation & execution guide
├── requirements.txt          # System package dependencies
├── .gitignore                # Global ignore filters (ignores local assets/databases)
│
├── Frontend/                 # User Interface & Visualizations Layer
│   ├── app.py                # Main Streamlit application & interactive panels
│   └── sarawak_flag.svg      # (Local Asset) Sarawak State Flag logo
│
└── Backend/                  # Scoring Logic & Data Persistence Layer
    ├── survey.py             # Math scoring engine & 75-item bilingual database
    └── sttb.db               # (Local Asset) Anonymous respondent SQL database
```

---

## Key Integrated Systems

### 1. Real-Time Bilingual Engine (English ↔ Bahasa Melayu)

- Switch between **English** and **Bahasa Melayu** instantly from the top-right header link without state loss or page reload.
- Fully localizes the 75 framework questions, live metrics, interactive maps, database collection drop-downs, and automatically computed personal digital trust report cards.
- Secure translation mapping ensures submissions are translated to standardized English categories before insertion into SQLite to maintain visualization pipeline consistency.

## Getting Started

### Prerequisites

Ensure Python 3.9+ is installed on your local machine.

### 1. Installation

Clone the repository and install all required python libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Execution

Run the local Streamlit application:

```bash
streamlit run Frontend/app.py
```

The app will automatically launch in your default web browser at `http://localhost:8501/`.

---

## The Five Trust Pillars of the Framework

1. **Transparency & Accessibility (Sidq & Tabayyun)**: Algorithmic openness, plain-language digital terms, and state-citizen information symmetry.
2. **Ethics & Responsibility (Amanah)**: Algorithmic fairness, lack of bias, and proactive digital stewardship.
3. **Privacy & Control (Tajassus & Haya)**: Empowered user agency over data, consent granularity, and preventing unauthorized intrusion.
4. **Security & Reliability (Itqan)**: Technical excellence, infrastructure resilience, and low digital services downtime.
5. **Digital Inclusion & Equity (Adl)**: Geographic coverage (urban vs rural), literacy support, and accessibility for marginalized groups.

---

## License & Credits

Developed as an academic R&D Final Year Project for UTS.
**Sarawak Tech-Trust Barometer © 2026.**
