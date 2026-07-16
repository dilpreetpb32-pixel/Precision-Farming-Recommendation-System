# 🌾 AI-Based Precision Farming Recommendation Engine

An intelligent machine learning-powered web application that recommends the most suitable crops and fertilizers based on soil properties and environmental conditions.

Built using **Python**, **Scikit-learn**, and **Streamlit**.

## 📖 Project Overview

Agriculture plays a vital role in food production and economic development. Selecting the right crop and fertilizer is essential for maximizing productivity while minimizing resource wastage.

The **AI-Based Precision Farming Recommendation Engine** assists farmers by analyzing soil characteristics and environmental parameters to provide intelligent recommendations.

The application consists of two machine learning modules:

- 🌾 Crop Recommendation System
- 🌱 Fertilizer Recommendation System

Both modules are deployed through an interactive Streamlit dashboard, enabling users to receive instant recommendations.

## ✨ Features

- 🌾 Crop Recommendation using Machine Learning
- 🌱 Fertilizer Recommendation using Machine Learning
- 📊 Prediction Confidence Scores
- 📈 Top 5 Recommendations
- 🤖 Random Forest Models
- ⚡ Interactive Streamlit Dashboard
- 📱 User-Friendly Interface

## 🛠️ Technology Stack

### Programming Language

- Python

### Machine Learning

- Scikit-learn
- Random Forest
- Logistic Regression
- Decision Tree
- K-Nearest Neighbors
- Support Vector Machine

### Data Processing

- Pandas
- NumPy

### Visualization

- Matplotlib
- Seaborn

### Deployment

- Streamlit

### Model Storage

- Joblib

## 📂 Project Structure

```text
AI-Based Precision Farming Recommendation Engine/
│
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 1_Crop_Recommendation.py
│       └── 2_Fertilizer_Recommendation.py
│
├── data/
├── models/
├── notebooks/
├── images/
├── reports/
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 🤖 Machine Learning Pipeline

```
Data Collection
        │
        ▼
Data Cleaning & Preprocessing
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Feature Engineering
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Best Model Selection
        │
        ▼
Streamlit Deployment
```

## 📊 Dataset Information

### Crop Recommendation Dataset

Features:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

Target:

- Crop Label

---

### Fertilizer Recommendation Dataset

Features:

- Soil Type
- Soil pH
- Soil Moisture
- Organic Carbon
- Electrical Conductivity
- Nitrogen Level
- Phosphorus Level
- Potassium Level
- Temperature
- Humidity
- Rainfall
- Crop Type
- Crop Growth Stage
- Season
- Irrigation Type
- Previous Crop
- Region
- Fertilizer Used Last Season
- Yield Last Season

Target:

- Recommended Fertilizer

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Based-Precision-Farming-Recommendation-Engine.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Based-Precision-Farming-Recommendation-Engine
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS/Linux**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Launch the Streamlit dashboard using:

```bash
streamlit run app/Home.py
```

The application will automatically open in your default web browser.

The dashboard contains the following pages:

- 🏠 Home
- 🌾 Crop Recommendation
- 🌱 Fertilizer Recommendation

## 📈 Model Performance

Several machine learning algorithms were trained and evaluated for both recommendation systems.

Algorithms evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- K-Nearest Neighbors (KNN)
- Support Vector Machine (SVM)

### Final Selected Models

| Module | Selected Model |
|---------|----------------|
| Crop Recommendation | Random Forest |
| Fertilizer Recommendation | Random Forest |

Random Forest achieved the best overall performance based on Accuracy, Precision, Recall, F1-Score, and Confusion Matrix analysis, making it the most suitable model for deployment.

## 🚀 Future Enhancements

The following features can be added in future versions of the project:

- 🌦️ Weather API Integration
- 🛰️ Satellite Image Analysis
- 📱 Mobile Application
- 🌍 Multi-language Support
- ☁️ Cloud Deployment
- 📍 GPS-Based Farm Recommendations
- 📊 Advanced Data Visualization

## 👨‍💻 Author

**Dilpreet Kaur**

Bachelor of Science in Information Technology (B.Sc. IT)

Lovely Professional University

GitHub: https://github.com/dilpreetpb32-pixel