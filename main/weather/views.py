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
        c_name = request.POST.get('name')
        exist = str(requests.get(url.format(c_name, os.environ['API_KEY'])).json().get('cod')) # checking code
        cityexists = City.objects.filter(name=c_name)
        if not cityexists and exist == '200':
            form.save()

    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    try:
        for city in cities:
            r = requests.get(url.format(city, os.environ['API_KEY'])).json()

            main = r.get('main')
            weather = r.get('weather')[0]

            city_weather = {
                'city': city.name,
                'temperature': main['temp'],
                'description': weather['description'],
                'icon': weather['icon'],
            }

            weather_data.append(city_weather)
    except KeyError as ke:
        raise "Key Error at: {}".format(ke)
    except Exception as e:
        raise "Exception at: {}".format(e)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)
