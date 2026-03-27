# 🦅 UliteTrade: AI-Augmented QA Automation Framework
**Architect:** Miguel Bautista (@miguelbautistag)
**Context:** Regional Exchange Integration (OMS) - Simulation

---

## 🚀 Overview
A high-concurrency automation ecosystem designed for the 2026 Agentic Testing landscape. This framework validates **Cross-Border Order Management Systems (OMS)** by synchronizing Playwright UI interactions with PostgreSQL Data Integrity checks.

## 🏛️ The 4 Architectural Pillars
1. **OBSERVABILITY:** Automated Trace/HTML reports for every failure (RCA-ready).
2. **DATA INTEGRITY:** Every UI trade is validated via SQL:
   - `SELECT o.status FROM orders o JOIN products p ON o.pid = p.id WHERE p.sku = 'ECOPETROL.CB'`
3. **SHIFT-RIGHT:** CI/CD via GitHub Actions with ephemeral Postgres service containers.
4. **CONTRACT TESTING:** Validates API schemas to ensure FE/BE alignment.

## 📁 Key Directories
- `.github/workflows/`: CI/CD Pipeline (Postgres + Playwright).
- `data/`: SQL seed scripts and market data payloads.
- `pages/`: Page Object Model (Logic-only).
- `tests/`: Functional and Data-Integrity test suites.

## 🛠 Setup & Execution
1. **Environment:** `source venv/bin/activate && pip install -r requirements.txt`
2. **Database:** `sudo -u postgres psql -f data/seed_market.sql`
3. **Run Suite:** `pytest tests/test_orders.py --html=report.html`

## 🤖 AI-Agent Integration (Gemini Architect)
This framework is mentored by a custom **AI/QA Architect**. 
- **Plan:** `/plan [scenario]` generates architecturally sound Pytest code.
- **Review:** `/review [file]` triggers a "Good/Bad/Ugly" audit based on `QA_CODING_STANDARDS.md`.

## ☕ Java Transition Roadmap
Aligned with `JAVA_TRANSITION_MAP.csv`, this Python logic maps 1:1 to:
- **Pytest** ➡️ **TestNG / JUnit 5**
- **Playwright (Py)** ➡️ **Playwright (Java)**
- **Psycopg2** ➡️ **JDBC / Spring Data JPA**
