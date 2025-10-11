from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
import datetime
import requests
def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=54155c4f2642e2512062a76af38e5cf9"
    weather_params = {'units': 'metric'}

    # Google Custom Search API
    API_KEY = 'AIzaSyBy71vZ-_pEfRVJR0cl8sDHeoHDyUk9xrI'
    SEARCH_ENGINE_ID = '2071d33066d48496b'
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = "image"
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # Default fallback image
    image_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1350&q=80"

    try:
        # Add timeouts so requests don't hang forever
        city_data = requests.get(city_url, timeout=5).json()
        search_items = city_data.get("items")
        if search_items:
            image_url = search_items[0]['link']
    except Exception as e:
        print("Image API error:", e)

    try:
        weather_data = requests.get(weather_url, params=weather_params, timeout=5).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        context = {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occured': False,
            'image_url': image_url
        }

    except Exception as e:
        print("Weather API error:", e)
        messages.error(request, 'Entered data is not available')
        day = datetime.date.today()
        context = {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occured': True,
            'image_url': image_url
        }

    template = loader.get_template("home.html")
    return HttpResponse(template.render(context, request))






# def home(request) :
#     if 'city' in request.POST :
#         city=request.POST['city']
#     else :
#         city='indore'
#     url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=54155c4f2642e2512062a76af38e5cf9"
#     PARAMS={'units':'metric'}

#     API_KEY='AIzaSyBy71vZ-_pEfRVJR0cl8sDHeoHDyUk9xrI'
#     SEARCH_ENGINE_ID='2071d33066d48496b'
#     query=city+ "1920x1080"
#     page=1
#     start=(page-1)*10+1
#     searchType="image"
#     city_url=f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
#     data=requests.get(city_url).json()
#     count=1
#     search_items=data.get("items")
#     search_items = data.get("items")
#     if search_items and len(search_items) > 0:
#         image_url = search_items[0]['link']
#     else:
#         image_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80"  # fallback image

#     try :
#         data=requests.get(url,PARAMS).json()
#         description=data['weather'][0]['description']
#         icon=data['weather'][0]['icon']
#         temp=data['main']['temp']
#         day=datetime.date.today()

#         context={'description':description,'icon':icon,'temp':temp,'day':day,'city':city,'exception_occured':False,'image_url':image_url}

#         template=loader.get_template("home.html")
#         return HttpResponse(template.render(context,request))
#     except :
#         exception_occured=True
#         messages.error(request,'Entered data is not availble')
#         day=datetime.date.today()
#         context={'description':'clar sky','icon':'01d','temp':25,'day':day,'city':'indore','exception_occured':True,'image_url':image_url}

#         template=loader.get_template("home.html")
#         return HttpResponse(template.render(context,request))

# Create your views here.
