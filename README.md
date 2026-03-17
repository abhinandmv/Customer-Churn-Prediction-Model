# 📡 Customer Churn Prediction

A machine learning web app that predicts whether a telecom customer is likely to churn, built with **Streamlit** and **scikit-learn**.

🔗 **Live Demo** → [your-app.streamlit.app](https://your-app.streamlit.app) *(update after deployment)*

---

## 📸 Preview

> Add a screenshot here after deployment!

---

## 🚀 Features

- Predicts customer churn in real-time using a trained ML model
- Clean, dark-themed UI with custom CSS
- Displays churn probability with a visual progress bar
- Covers 19 customer attributes across demographics, services, and billing

---

## 🧠 Model Info

| Detail | Value |
|---|---|
| Algorithm | *(e.g. Random Forest / XGBoost / Logistic Regression)* |
| Dataset | [Telco Customer Churn – Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| Target | `Churn` (Yes / No) |
| Input Features | 19 |

---

## 📁 Project Structure

```
├── main.py               # Streamlit app
├── best_model.pkl       # Trained ML model
├── encoder.pkl          # Label encoders for categorical features
├── scaler.pkl           # StandardScaler for numerical features
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ⚙️ Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/abhinandmv/Customer-Churn-Prediction-Model
cd Customer-Churn-Prediction-Model
```

**2. Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run main.py
```

Open your browser at → `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub → **Create app**
4. Select your repo, branch `main`, file `app.py`
5. Click **Deploy** ✅

---

## 📦 Requirements

```
streamlit
pandas
scikit-learn
```

---

## 📊 Input Features

| Feature | Type | Description |
|---|---|---|
| `gender` | Categorical | Male / Female |
| `SeniorCitizen` | Binary | 0 = No, 1 = Yes |
| `Partner` | Categorical | Has a partner |
| `Dependents` | Categorical | Has dependents |
| `tenure` | Numeric | Months with the company |
| `PhoneService` | Categorical | Has phone service |
| `MultipleLines` | Categorical | Has multiple lines |
| `InternetService` | Categorical | DSL / Fiber optic / No |
| `OnlineSecurity` | Categorical | Has online security |
| `OnlineBackup` | Categorical | Has online backup |
| `DeviceProtection` | Categorical | Has device protection |
| `TechSupport` | Categorical | Has tech support |
| `StreamingTV` | Categorical | Streams TV |
| `StreamingMovies` | Categorical | Streams movies |
| `Contract` | Categorical | Month-to-month / 1yr / 2yr |
| `PaperlessBilling` | Categorical | Uses paperless billing |
| `PaymentMethod` | Categorical | Payment type |
| `MonthlyCharges` | Numeric | Monthly bill amount |
| `TotalCharges` | Numeric | Total amount billed |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).