# 💧 AquaSave — Smart Water Usage Dashboard

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-brightgreen.svg)](https://streamlit.io/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Made with Love](https://img.shields.io/badge/Made%20with-Love-red.svg)](#)

AquaSave is a **Green-AI demo project** that simulates household water consumption, applies machine learning models to forecast usage, and provides an interactive **Streamlit dashboard** to visualize savings at both household and city level. It also generates **eco-impact PDF reports**.

---

## 🚀 Features

- Synthetic water usage data generator  
- Preprocessing pipeline with time-based features  
- Lightweight **Linear Regression** and **Random Forest** forecasting models (Green-AI settings)  
- Interactive **Streamlit app** with:  
  - Household-level history and 7-day forecast  
  - Usage reduction simulation  
  - City-wide savings impact  
  - PDF report export  

---

## 📂 Project Structure

```
aqua-save/
├─ .vscode/
│  └─ launch.json
├─ data/
├─ models/
├─ src/
│  ├─ generate_data.py
│  ├─ preprocess.py
│  ├─ train_model.py
│  ├─ app.py
├─ requirements.txt
└─ README.md
```

---

## ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/aqua-save.git
   cd aqua-save
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Project

You can use the provided **VS Code launch configs** or run manually:

1. **Generate synthetic data**  
   ```bash
   python src/generate_data.py
   ```

2. **Preprocess data**  
   ```bash
   python src/preprocess.py
   ```

3. **Train models**  
   ```bash
   python src/train_model.py
   ```

4. **Launch Streamlit dashboard**  
   ```bash
   streamlit run src/app.py
   ```

Dashboard will open at [http://localhost:8501](http://localhost:8501).

---

## 📊 Dashboard Preview

### Household View  
📈 Daily usage history & 7-day forecast  

### City-Level Impact  
🌍 Aggregated savings visualization  

### PDF Report  
📄 One-click eco-impact report  

👉 *(Add screenshots here — e.g., dashboard charts, city-level plots, PDF export preview)*  

---

## 🛠️ Tech Stack

- **Python** (pandas, numpy, scikit-learn, joblib, matplotlib)  
- **Streamlit** for interactive dashboard  
- **ReportLab** for PDF export  

---

## 📄 License

This project is licensed under the MIT License — feel free to use and adapt.  

---

💡 *Run `Generate Data → Preprocess → Train Model → Streamlit App` in sequence if setting up from scratch.*  
