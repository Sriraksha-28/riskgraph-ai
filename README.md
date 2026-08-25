# RiskGraph AI

RiskGraph AI is an end-to-end fraud risk detection and investigation platform that combines graph-based risk features, rule-based scoring, and machine learning to identify potentially suspicious users and transactions.

## Overview

The system analyzes users and transactions to identify suspicious behavior using:

- Graph-based relationship analysis
- Rule-based risk scoring
- Machine learning predictions
- Combined final risk scoring
- Interactive Streamlit dashboard
- User-level investigation and transaction analysis

The goal is to provide both automated risk detection and an interface for investigating suspicious activity.

---

## Key Features

### Risk Detection

- Rule-based risk scoring
- Machine learning suspicious probability
- Final combined risk score
- LOW / MEDIUM / HIGH risk classification

### Graph Analysis

The system analyzes relationships between:

- Users
- Devices
- Merchants

Graph features include:

- Shared devices
- Device-user connections
- Transaction velocity
- Short-window transaction activity
- Merchant concentration

### Dashboard

The Streamlit dashboard contains:

1. **Overview**
   - Risk distribution
   - User statistics
   - Suspicious activity
   - Priority users

2. **Risk Explorer**
   - Explore users by risk level
   - Compare risk scores and ML probabilities

3. **User Investigation**
   - Investigate individual users
   - Risk reasons
   - Connected devices
   - Connected merchants
   - Shared-device users
   - Suspicious transactions

4. **Transactions**
   - Transaction analysis
   - Suspicious/normal filtering
   - Location filtering
   - Transaction statistics

5. **ML Insights**
   - Model evaluation
   - Feature importance
   - Rule-based vs ML comparison

6. **Graph Analysis**
   - Device sharing
   - Merchant concentration
   - User/device/merchant relationships

7. **About**
   - Project information and system overview

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and data processing |
| Pandas | Data processing and CSV analysis |
| NumPy | Numerical computation |
| Scikit-learn | Machine learning |
| NetworkX | Graph-based analysis |
| Joblib | ML model storage and loading |
| Streamlit | Interactive dashboard |

---

## Project Structure

```text
riskgraph-ai/
│
├── data/
│   ├── users.csv
│   ├── transactions.csv
│   ├── user_features.csv
│   ├── user_risk_scores.csv
│   ├── ml_risk_predictions.csv
│   ├── final_risk_results.csv
│   └── ...
│
├── models/
│   └── risk_model.pkl
│
├── src/
│   ├── dashboard.py
│   ├── app.py
│   ├── ui_utils.py
│   ├── validate_data.py
│   ├── validate_pipeline.py
│   └── pages/
│       ├── 1_Overview.py
│       ├── 2_Risk_Explorer.py
│       ├── 3_User_Investigation.py
│       ├── 4_Transactions.py
│       ├── 5_ML_Insights.py
│       ├── 6_Graph_Analysis.py
│       └── 7_About.py
│
├── requirements.txt
└── README.md