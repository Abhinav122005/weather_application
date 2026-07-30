from pyexpat.errors import messages

from django.shortcuts import redirect, render
import requests
import json
from datetime import datetime
from . models import FavoriteCity, SearchHistory
from django.conf import settings
# Create your views here.



def home(req):
    lat = req.GET.get("lat")
    lon = req.GET.get("lon")
    city = req.GET.get("city", "")

    if lat and lon:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={settings.API_KEY}&units=metric"
        )
    else:
        if not city:
            city = "Hyderabad"
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={settings.API_KEY}&units=metric"
        )

    context = {}

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            context = {
                "city": data["name"],
                "temperature": round(data["main"]["temp"]),
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "icon": data["weather"][0]["icon"],
            }
        else:
            context["error"] = "City not found."

    except Exception:
        context["error"] = "Unable to fetch weather."

    # Fetch popular cities dynamically
    popular_cities = ["Hyderabad", "Delhi", "Mumbai", "London"]
    popular_weather = []
    for pc in popular_cities:
        try:
            res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={pc}&appid={settings.API_KEY}&units=metric", timeout=5)
            d = res.json()
            if d.get("cod") == 200:
                popular_weather.append({
                    "city": d["name"],
                    "temp": round(d["main"]["temp"]),
                    "description": d["weather"][0]["description"].title(),
                    "icon": d["weather"][0]["icon"],
                })
        except:
            pass
            
    context["popular_weather"] = popular_weather

    return render(req, 'index.html', context)


from datetime import datetime
import requests


def dashboard(request):

    if "user_id" not in request.session:
        return redirect("login")

    username = request.session.get("username")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    city = request.GET.get("city", "")
    unit = request.GET.get("unit", "metric")

    context = {}

    forecast = []
    hourly_forecast = []
    weather_alerts = []
    chart_labels = []
    chart_temperatures = []
    rain_labels = []
    rain_data = []

    favorites = FavoriteCity.objects.filter(
        user_id=request.session["user_id"]
    )

    history = SearchHistory.objects.filter(
        user_id=request.session["user_id"]
    ).order_by("-searched_at")[:10]

    # ================= CURRENT WEATHER ================= #

    if lat and lon:
        current_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={settings.API_KEY}&units={unit}"
        )
    else:
        if not city:
            city = "Hyderabad"
        current_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={settings.API_KEY}&units={unit}"
        )

    try:

        response = requests.get(current_url, timeout=10)

        data = response.json()

        if data.get("cod") == 200:

            context.update({

                "city": data["name"],

                "temperature": round(data["main"]["temp"]),

                "description": data["weather"][0]["description"].title(),

                "humidity": data["main"]["humidity"],

                "wind": data["wind"]["speed"],

                "feels_like": round(data["main"]["feels_like"]),

                "visibility": data["visibility"] // 1000,

                "icon": data["weather"][0]["icon"],

                "weather_icon_type": data["weather"][0]["main"].lower(),

                "latitude": data["coord"]["lat"],

                "longitude": data["coord"]["lon"],

            })

            # ---------- Favorite Check ---------- #

            context["is_favorite"] = FavoriteCity.objects.filter(

                user_id=request.session["user_id"],

                city=data["name"]

            ).exists()

            # ---------- Search History ---------- #

            last_search = SearchHistory.objects.filter(

                user_id=request.session["user_id"]

            ).order_by("-searched_at").first()

            if not last_search or last_search.city != data["name"]:

                SearchHistory.objects.create(

                    user_id=request.session["user_id"],

                    city=data["name"]

                )

            # ---------- Sunrise / Sunset ---------- #

            context["sunrise"] = datetime.fromtimestamp(

                data["sys"]["sunrise"]

            ).strftime("%I:%M %p")

            context["sunset"] = datetime.fromtimestamp(

                data["sys"]["sunset"]

            ).strftime("%I:%M %p")

            # ---------- Weather Alerts ---------- #

            weather_condition = data["weather"][0]["main"].lower()
            weather_description = data["weather"][0]["description"].lower()
            high_temperature = 35 if unit == "metric" else 95

            if weather_condition == "thunderstorm":
                weather_alerts.append({
                    "level": "danger",
                    "title": "Thunderstorm Alert",
                    "message": "Thunderstorms are expected. Avoid exposed outdoor areas when possible.",
                })

            if weather_condition == "rain" and "heavy" in weather_description:
                weather_alerts.append({
                    "level": "primary",
                    "title": "Heavy Rain Alert",
                    "message": "Heavy rain is reported for this location. Plan travel with care.",
                })

            if data["main"]["temp"] >= high_temperature:
                weather_alerts.append({
                    "level": "warning",
                    "title": "High Temperature Alert",
                    "message": "Temperatures are unusually high. Stay hydrated and limit prolonged sun exposure.",
                })

            # ---------- AQI ---------- #

            lat = data["coord"]["lat"]

            lon = data["coord"]["lon"]

            aqi_url = (

                f"https://api.openweathermap.org/data/2.5/air_pollution"

                f"?lat={lat}&lon={lon}&appid={settings.API_KEY}"

            )

            aqi_response = requests.get(

                aqi_url,

                timeout=10

            )

            aqi_data = aqi_response.json()

            if "list" in aqi_data and aqi_data["list"]:

                aqi = aqi_data["list"][0]["main"]["aqi"]

                context["aqi"] = aqi

                context["aqi_status"] = {

                    1: "Good 😊",

                    2: "Fair 🙂",

                    3: "Moderate 😐",

                    4: "Poor 😷",

                    5: "Very Poor ☠️"

                }.get(aqi, "Unknown")

                if aqi >= 4:
                    weather_alerts.append({
                        "level": "danger",
                        "title": "Poor Air Quality",
                        "message": "Air quality is poor. Consider limiting strenuous outdoor activity.",
                    })

        else:

            context["error"] = "City not found."

    except Exception as e:

        print(e)

        context["error"] = "Unable to fetch weather."

    # ================= FORECAST ================= #

    if lat and lon:
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={lat}&lon={lon}&appid={settings.API_KEY}&units={unit}"
        )
    else:
        forecast_url = (
            f"https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={settings.API_KEY}&units={unit}"
        )

    try:

        forecast_response = requests.get(
            forecast_url,
            timeout=10
        )

        forecast_data = forecast_response.json()

        if str(forecast_data.get("cod")) == "200":

            # ---------- 5-Day Forecast ---------- #
            for item in forecast_data["list"][::8][:5]:
                day_str = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%a")
                forecast.append({
                    "date": day_str,
                    "temp": round(item["main"]["temp"]),
                    "description": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"],
                })
                rain_labels.append(day_str)
                rain_data.append(round(item.get("pop", 0) * 100))

            # ---------- Hourly Forecast ---------- #
            for item in forecast_data["list"][:8]:
                time_str = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
                temp_val = round(item["main"]["temp"])
                hourly_forecast.append({
                    "time": time_str,
                    "temp": temp_val,
                    "description": item["weather"][0]["description"].title(),
                    "icon": item["weather"][0]["icon"],
                })
                chart_labels.append(time_str)
                chart_temperatures.append(temp_val)

    except Exception as e:
        print(e)

    # ================= CONTEXT ================= #
    context["forecast"] = forecast
    context["hourly_forecast"] = hourly_forecast
    context["favorites"] = favorites
    context["history"] = history
    context["username"] = username
    context["unit"] = unit
    context["weather_alerts"] = weather_alerts
    
    context["chart_labels"] = json.dumps(chart_labels)
    context["chart_temperatures"] = json.dumps(chart_temperatures)
    context["rain_labels"] = json.dumps(rain_labels)
    context["rain_data"] = json.dumps(rain_data)

    return render(request,"dashboard.html",context)
def add_favorite(req):
    if 'user_id' not in req.session:
        return redirect('login')

    if req.method =="POST":
        city = req.POST.get("city")

        FavoriteCity.objects.get_or_create(
            user_id=req.session["user_id"],
            city=city
        )
    return redirect('dashboard')


def delete_favorite(request, city_id):

    if "user_id" not in request.session:
        return redirect("login")

    try:
        favorite = FavoriteCity.objects.get(
            id=city_id,
            user_id=request.session["user_id"]
        )

        favorite.delete()
        messages.success(request, "City removed from favorites.")

    except FavoriteCity.DoesNotExist:
        messages.error(request, "Favorite city not found.")

    return redirect("dashboard")


def current_location(request):

    if "user_id" not in request.session:
        return redirect("login")

    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={settings.API_KEY}&units=metric"
    )

    response = requests.get(url)

    data = response.json()

    city = data["name"]

    return redirect(f"/dashboard/?city={city}")
