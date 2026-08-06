# 🌤️ WeatherHub - Advanced Django Weather Application

Welcome to **WeatherHub**, a modern, feature-rich weather forecasting web application built with Django and Python. 

This application goes beyond simple weather tracking by offering a premium **Glassmorphic UI**, dynamic interactive charts, automatic geolocation, user authentication, and personalized weather alerts—all wrapped in a sleek, responsive design that supports both Light and Dark modes!

## ✨ Key Features

- **📍 Auto-Detect Location (Geolocation):** Instantly fetches the exact weather for your current GPS location the moment you open the app, or anytime you click the location target button.
- **📈 Dynamic Data Visualization (Chart.js):**
  - **Temperature Trends:** A smooth line chart displaying the upcoming 24-hour temperature forecast.
  - **Chances of Rain:** A customized bar chart mapping out the probability of precipitation over the next 5 days.
  - **Air Quality Index (AQI):** A responsive half-doughnut gauge that dynamically updates its color based on air quality severity (Good to Poor).
  - **Wind Status:** An animated visual wave chart for current wind data.
- **🎨 Premium UI / UX:** Deep glassmorphism aesthetics with dynamic background blurring, sleek hover effects, and a seamless toggle between Dark Mode and Light Mode.
- **⚡ Real-Time Data:** Live API integration with OpenWeatherMap for Current, Hourly, and 5-Day forecasts.
- **🌍 Dynamic Popular Cities:** Instantly see the weather in major cities (Hyderabad, Delhi, Mumbai, London) right on the home page.
- **🔐 User Authentication:** Secure registration, login, and profile management.
- **⭐ Personalized Dashboard:** Save your "Favorite Cities" for quick access and view your recent "Search History".
- **⚠️ Weather Alerts:** Automated context-aware alerts to warn you about Thunderstorms, Heavy Rain, Extreme Heat, or Poor Air Quality.

## 🛠️ Technology Stack

- **Backend:** Python, Django 4.x
- **Frontend:** HTML5, CSS3, JavaScript
- **Frameworks / Libraries:** Bootstrap 5.3, Chart.js, FontAwesome
- **API Integration:** OpenWeatherMap API (Weather, Forecast, Air Pollution)
- **Database:** SQLite (default for development)

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/weather_application.git
   cd weather_application
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenWeatherMap API Key:**
   Open `weather_app/views.py` and ensure your `API_KEY` is configured:
   ```python
   API_KEY = "your_openweathermap_api_key_here"
   ```
   *(Note: For production environments, always store API keys in environment variables (.env).*

5. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application:**
   Open your browser and navigate to `http://127.0.0.1:8000/`.

## 📸 Screenshots

*(Consider adding screenshots of your Light Mode, Dark Mode, and Dashboard Charts here to showcase the beautiful UI!)*

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
