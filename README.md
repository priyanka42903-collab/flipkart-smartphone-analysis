# Flipkart Smartphone Price Intelligence System

> An automated price tracking system that monitors 268 smartphone 
> listings on Flipkart daily — detecting MRP inflation, price drops, 
> and brand pricing strategies using Python, SQL, and Power BI.

## 🚨 Key Findings

- **39 products** caught with changing MRP values in 7 days — 
  Realme P4x MRP jumped ₹17,000 while selling price barely changed, 
  making a 2% real discount appear as 35%
- **MOTOROLA g37 power** dropped ₹6,000 (27.3%) in just 7 days — 
  biggest price drop detected
- **OnePlus Nord CE6 Lite** changed price 26 times in 7 days — 
  nearly 4 times per day
- **Mid-range segment (₹10K-20K)** dominates with 41.84% market share 
  and highest average discounts (23.2%)
- **HMD (Nokia)** is the hidden gem — 3rd highest rating (4.5) at 
  budget average price (₹17,499) — most overlooked brand
- **Apple and iQOO** follow low-discount strategy (<10%) while 
  **Realme** inflates MRP to show fake 35%+ discounts

## 📊 Dashboard

![Market Overview] 
(<img width="1122" height="632" alt="Screenshot 2026-07-24 171229" src="https://github.com/user-attachments/assets/3b2e80c8-bf09-4747-a170-0690e57ee532" />).

![MRP Deception]
(<img width="1137" height="638" alt="Screenshot 2026-07-24 171252" src="https://github.com/user-attachments/assets/aa6af270-fa61-4f88-bbb2-65eb180c7921" />)

![Price Intelligence]
(<img width="1122" height="633" alt="Screenshot 2026-07-24 171307" src="https://github.com/user-attachments/assets/4e00783f-7ede-4eee-8cec-fd547bf26793" />)

![Buyer Intelligence]
(<img width="1120" height="635" alt="Screenshot 2026-07-24 171332" src="https://github.com/user-attachments/assets/d2f492c5-0ff7-4410-b2a2-ce1fa9e671ba" />)


## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python + BeautifulSoup | Web scraping Flipkart listings |
| Pandas | Data cleaning and transformation |
| SQLite + SQL | Data storage and analysis queries |
| Power BI | Interactive dashboard |
| Jupyter Notebook | Analysis and documentation |

## 📁 Project Structure
flipkart-smartphone-analysis/
├── src/
│ ├── scraper.py # Flipkart scraper
│ └── database.py # SQLite loader
├── notebooks/
│ ├── data_cleaning.ipynb # Cleaning pipeline
│ └── sql_analysis.ipynb # 8 SQL queries + findings
├── dashboard/ # Power BI .pbix file
├── data/
│ ├── raw/ # Daily scraped CSVs (gitignored)
│ └── processed/ # Cleaned data (gitignored)
└── requirements.txt

## 🚀 How to Reproduce

```bash
# 1. Clone repo
git clone https://github.com/priyanka42903-collab/flipkart-smartphone-analysis
cd flipkart-smartphone-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Collect data (run daily for multiple days)
python src/scraper.py

# 4. Clean data
# Run notebooks/data_cleaning.ipynb

# 5. Load database
python src/database.py

# 6. Run SQL analysis
# Run notebooks/sql_analysis.ipynb
```

---

## 📈 Data Collection

- **Source:** Flipkart.com smartphone listings (live scraped)
- **Period:** June 30 – July 6, 2026 (7 days)
- **Products tracked:** 268 unique smartphones
- **Total observations:** 810 rows after deduplication
- **Brands covered:** 15 brands including Samsung, Apple, Realme, 
  Motorola, POCO, Vivo, OnePlus

  ## ⚠️ Data Notes

- Raw CSV files are gitignored — run scraper to collect fresh data
- 39 products showed MRP changes across the tracking period
- Only 31 products appeared consistently across all 7 days — 
  Flipkart rotates search results daily
- Color variants deduplicated — one entry per model per day

---

## 🔗 Connect

Built by **Priyanka Gupta** — 3rd year student building real-world 
data projects
