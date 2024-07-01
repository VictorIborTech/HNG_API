from django.http import JsonResponse
import requests

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('REMOTE_ADDR')
    
    # Get location using IP address
    try:
        response = requests.get(f'https://ipapi.co/{client_ip}/json/')
        data = response.json()
        city = data.get('city', 'Unknown')
    except requests.RequestException:
        city = 'Unknown'

    # Get temperature
    temperature = 'unknown'
    try:
        weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=090301aefbe58035a800fb5b5589faa0&units=metric')
        weather_data = weather_response.json()
        if 'main' in weather_data and 'temp' in weather_data['main']:
            temperature = weather_data['main']['temp']
        else:
            print(f"Unexpected weather data format: {weather_data}")  # For debugging
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")  # For debugging

    return JsonResponse({
        'client_ip': client_ip,
        'location': city,
        'greeting': f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}"
    })