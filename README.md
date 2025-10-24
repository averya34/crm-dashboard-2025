# 📊 CRM Dashboard 2025

A complete end-to-end CRM analytics dashboard using Google Drive as the data source and Streamlit for visualization.

## 🚀 Setup Instructions

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the Streamlit dashboard:**
```bash
streamlit run app.py
```

## 📁 Repository Structure

```
crm-dashboard-2025/
├── data/                          # Place your CSV files here
├── notebooks/
│   └── upload_and_clean.ipynb     # Colab notebook for data processing
├── app.py                         # Streamlit dashboard
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 📓 Data Processing Workflow

### Using Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/averya34/crm-dashboard-2025/blob/main/notebooks/upload_and_clean.ipynb)

1. Open `upload_and_clean.ipynb` in Google Colab
2. Mount your Google Drive
3. The notebook will list all CSVs in `/CRM_Dashboard_Exports/`
4. Manually select which files to process
5. The notebook will:
   - Clean and merge selected CSVs
   - Generate derived fields (Project, Lead Type)
   - Export to `combined_crm_leads.csv`

### Derived Fields Logic

**Project Mapping:**
- Maps "Interested: X" columns to unified Project field
- Projects: Vesper, The Code, Belvedere, Unspecified

**Lead Type Classification:**
- "Reengaged" if Last Assigned > Date Added
- "New" otherwise

## 📊 Dashboard Features

### Filters
- Project selection
- Source selection
- Lead Type (New vs Reengaged)
- Date type toggle (Date Added / Last Assigned)
- Date range selector

### Metrics
- 👥 Total Leads
- 🏗 Unique Projects
- 🌐 Unique Sources
- 🔁 Reengaged %

### Visualizations
- Leads by Project (bar chart)
- Leads by Source (pie chart)
- Lead Creation Timeline (line chart with frequency toggle)
- Reengagement Trend (new vs reengaged overlay)
- Raw data preview table

## 🎨 Visual Style

- Dark theme
- Emoji headers
- Full-width responsive layout
- Interactive Plotly charts

## 📂 Google Drive Setup

1. Create folder: `/CRM_Dashboard_Exports/` in your Google Drive
2. Upload your CRM CSV exports to this folder
3. Run the Colab notebook to process files
4. Copy `combined_crm_leads.csv` to the `/data/` folder in this repo

## 🔧 Requirements

- Python 3.7+
- streamlit
- pandas
- plotly
