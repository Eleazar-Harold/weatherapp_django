# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import os
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.

def index(request):
    # for Fahrenheit --> imperial
    # for Celsius --> metric
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        cityexists = City.objects.filter(name=request.POST.get('name'))
        if not cityexists:
            form.save()

    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city, os.environ['API_KEY'])).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)
