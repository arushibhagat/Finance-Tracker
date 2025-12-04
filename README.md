# 💰 My Finance Tracker

A Flask-based personal finance tracking web application built with **Flask**, **SQLite**, **Bootstrap**, and **Chart.js**.  
It helps manage daily expenses and incomes, analyze spending trends, filter transactions, and export data.

---

## 🚀 Features

### 📌 Core Functionalities
- Add, Edit, Delete financial transactions
- Custom categories
- Search and filter by:
  - Notes / Category text search
  - Category dropdown
  - Date range (start–end)
- Persistent storage using SQLite

### 📊 Dashboard Analytics
- Total Spent summary
- Category-wise spending chart (Pie chart)
- Monthly and Daily analysis charts
- Top spending category highlight

### 📦 Export
- Download filtered transactions as a **CSV file**
- Export respects active filters

### 🖥 UI & UX
- Clean modern Bootstrap UI
- Icon-based edit/delete buttons
- Toast notifications + Loader animations (UX polish)
- Responsive layout

---

## 📸 Screenshots

| Dashboard | Transactions |
|-----------|--------------|
| <img width="1919" height="869" alt="image" src="https://github.com/user-attachments/assets/8f162afe-ac1b-4972-bb35-00fa41f812dc" /> | <img width="1906" height="700" alt="image" src="https://github.com/user-attachments/assets/35136871-593b-4fe9-a80e-393b383539de" />

---

## 🏗 Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Flask (Python) |
| Database | SQLite |
| Frontend | Bootstrap 5, HTML, CSS, JS |
| Charts | Chart.js |
| Version Control | Git & GitHub |

---

## 📂 Project Structure
```
Finance-Tracker/
│
├── app.py                     # Main Flask application
├── database.db         # SQLite database file
├── requirements.txt           # Required Python dependencies
│
├── static/                    # Static assets
│   └── style.css              
│
├── templates/                 # HTML template files (Jinja2 templates)
│   ├── base.html              
│   ├── dashboard.html         
│   ├── history.html           
│   ├── add.html               
│   ├── edit.html              
│
└── README.md                  # Project documentation
```
---

## ⚙ Installation & Setup

### 1️⃣ Clone the Repository
```
bash git clone https://github.com/arushibhagat/Finance-Tracker.git
cd Finance-Tracker
```

### 2️⃣ Create and Activate Virtual Environment (Optional)
```
python -m venv venv
venv/Scripts/activate   # Windows
source venv/bin/activate  # macOS/Linux
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Run Project
```
python app.py
```

### 5️⃣ Open in Browser
http://127.0.0.1:5000


