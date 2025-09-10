# UrbanPulse - AI Route Advisor

UrbanPulse is a full-stack web application designed to predict and advise on urban traffic routes using a custom-trained machine learning model. The application provides a comparative analysis between Google's live traffic estimates and a predictive model based on historical patterns, location, and live weather data.

## Features

- **AI-Powered Route Advisor:** Fetches multiple alternative routes and uses a custom AI to recommend the fastest one.
- **Live Weather Integration:** Incorporates real-time weather data from OpenWeatherMap to make predictions more accurate.
- **Context-Aware Predictions:** The AI model is trained on time of day, day of week, specific road types (Highway, Arterial, Local), and weather conditions.
- **Interactive UI:** A futuristic, dark-themed dashboard built with Tailwind CSS.
- **Dynamic Map:** Visualizes all route options, highlighting the AI-recommended route and marking start/end points.
- **Google Places Autocomplete:** Provides a smooth user experience for entering locations.

## Tech Stack

- **Backend:** Python, Flask, Scikit-learn, Pandas, NumPy, Joblib, googlemaps, requests
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **APIs:** Google Maps Platform (Maps, Places, Directions), OpenWeatherMap
- **Development:** PyCharm, Jupyter Notebook for model training (R² Score: 0.97)

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/UrbanPulse-AI-Route-Advisor.git](https://github.com/your-username/UrbanPulse-AI-Route-Advisor.git)
   cd UrbanPulse-AI-Route-Advisor