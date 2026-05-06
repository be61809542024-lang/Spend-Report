# Procurement Spend Dashboard

## Project Overview
This project is an interactive procurement analytics dashboard built using Python and Streamlit. It helps visualize and analyze procurement expenditure patterns across departments, campuses, suppliers, and categories.

## Objectives
- Analyze procurement spending patterns
- Identify top suppliers and departments
- Track monthly expenditure trends
- Enable interactive filtering and search of procurement records

## Tools & Technologies
- Python
- Streamlit
- Pandas
- Plotly
- Excel (data source)

## Dataset
The dataset includes:
- LPO numbers
- Dates
- Suppliers
- Departments
- Campuses
- Classification categories
- Item descriptions
- Quantities and total cost

##  Features
- Interactive KPIs (Total spend, LPO count, averages)
- Search functionality (supplier & item-level search)
- Drill-down analysis by classification
- Department and campus analysis
- Monthly procurement trends
- Supplier ranking insights
- Detailed transaction table

## How to Run
```bash
pip install -r requirements.txt
python -m streamlit run proc_spend_report.py
