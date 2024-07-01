
# TESTING CODE PHASE

# from django.http import JsonResponse
# import requests

# def hello(request):
#     visitor_name = request.GET.get('visitor_name', 'Guest')
#     client_ip = request.META.get('REMOTE_ADDR')
    
#     # Get location using IP address
#     try:
#         response = requests.get(f'https://ipapi.co/{client_ip}/json/')
#         data = response.json()
#         city = data.get('city', 'Unknown')
#     except requests.RequestException:
#         city = 'Unknown'

#     # Get temperature
#     temperature = 'unknown'
#     try:
#         weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=090301aefbe58035a800fb5b5589faa0&units=metric')
#         weather_data = weather_response.json()
#         if 'main' in weather_data and 'temp' in weather_data['main']:
#             temperature = weather_data['main']['temp']
#         else:
#             print(f"Unexpected weather data format: {weather_data}")  # For debugging
#     except requests.RequestException as e:
#         print(f"Error fetching weather data: {e}")  # For debugging

#     return JsonResponse({
#         'client_ip': client_ip,
#         'location': city,
#         'greeting': f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}"
#     })


# REAL CODE

from django.http import JsonResponse
import requests
import logging

logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = get_client_ip(request)

    logger.info(f"Received request from IP: {client_ip}")

    # Get location using IP address
    city = 'Unknown'
    try:
        # Using ipinfo.io which is allowed by PythonAnywhere
        response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        data = response.json()
        city = data.get('city', 'Unknown')
        logger.info(f"Location data: {data}")
    except requests.RequestException as e:
        logger.error(f"Error fetching location data: {e}")

    # Get temperature
    temperature = 'unknown'
    try:
        weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=090301aefbe58035a800fb5b5589faa0&units=metric')
        weather_data = weather_response.json()
        if 'main' in weather_data and 'temp' in weather_data['main']:
            temperature = weather_data['main']['temp']
        else:
            logger.error(f"Unexpected weather data format: {weather_data}")
    except requests.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")

    response_data = {
        'client_ip': client_ip,
        'location': city,
        'greeting': f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}"
    }

    logger.info(f"Sending response: {response_data}")

    return JsonResponse(response_data)


