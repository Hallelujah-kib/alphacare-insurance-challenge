# AlphaCare Insurance Risk Analytics & Predictive Modeling

**Optimizing marketing strategies and premium pricing through data-driven risk analysis of South African car insurance claims.**

## Business Objective
AlphaCare Insurance Solutions (ACIS) aims to identify low-risk customer segments and optimize premium pricing using historical claim data (Feb 2014 - Aug 2015). Key deliverables:
1. **EDA** to uncover risk/profitability patterns
2. **A/B Hypothesis Testing** for risk drivers
3. **Predictive Models** for claim severity/premium optimization
4. **Data Version Control** for reproducibility

## Data
- **Source**: Internal claims dataset (structure detailed in `Week 3 Challenge.pdf`)
- **Location**: `data/raw/`
- **Key Features**:
  - Policy details (`SumInsured`, `CoverType`)
  - Client demographics (`Gender`, `Province`)
  - Vehicle specs (`Make`, `Model`, `CubicCapacity`)
  - Financials (`TotalPremium`, `TotalClaims`)

## Project Structure
alphacare-insurance-challenge/
├── data/ # DVC-tracked datasets
│ ├── processed/ # Cleaned data
│ └── raw/ # Original data (git-ignored)
├── docs/ # Reports & documentation
├── notebooks/ # Exploratory analysis
│ ├── insurance_data_eda.ipynb
│ └── data_version_control.ipynb
├── scripts/ # Utility scripts
├── src/ # Core modules
│ ├── analysis/ # Hypothesis testing
│ ├── data_scripts/ # Data processing
│ ├── modeling/ # ML models
│ └── utils/ # Config/logger helpers
├── tests/ # Unit tests
├── .dvc/ # DVC configs
├── dxc_storage/ # Local DVC remote
├── requirements.txt # Python dependencies
└── run_pipeline.py # Main execution script


## Setup
1. **Clone repository**:
   ```bash
   git clone https://github.com/Hallelujah-kib/alphacare-insurance-challenge.git
   cd alphacare-insurance-challenge
2. **Install dependencies**:
pip install -r requirements.txt
3. **Initialize DVC**
dvc pull  # Fetches data from remote storage

Usage
Task	Command/Notebook	Output
EDA	notebooks/insurance_data_eda.ipynb	Reports/figures in reports/figures/
DVC Tracking	dvc add data/raw/new_data.csv	Metadata in .dvc files
Run Pipeline	python run_pipeline.py	Processed data & models



---

### **Placeholder Completion Guide**  
Fill these in your report/README:

| Placeholder               | Where to Find                                                                 |
|---------------------------|-------------------------------------------------------------------------------|
| `{overall loss ratio}`    | Calculate `TotalClaims.sum() / TotalPremium.sum()` from EDA                   |
| `{Top 3 high-risk provinces}` | Sort provinces by loss ratio in `insurance_data_eda.ipynb`                |
| `{Key Insight}`           | Top observation from EDA (e.g., "Men show 15% higher claim severity")         |
| `{Missing value details}` | Output from `notebooks/insurance_data_eda.ipynb` data quality checks          |
| `{Images}`                | Use the 3 plots you created in Task-1 (ensure paths match `reports/figures/`) |
