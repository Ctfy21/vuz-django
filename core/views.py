import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .decorators import unauthenticated_user
from django.contrib import messages
from .models import *
from django.conf import settings
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from .forms import CityForm, CreateUserForm


@unauthenticated_user
def loginUser(request):
      
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')                
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Имя пользователя или пароль неверны!')
    context = {}
    return render(request, 'core/login.html', context)


@login_required(login_url="loginUser")
def logoutUser(request):
    logout(request)
    return redirect('loginUser')


@unauthenticated_user
def registerUser(request):
    
    creation_form = CreateUserForm()
    if request.method == 'POST':
        creation_form = CreateUserForm(request.POST)
        if creation_form.is_valid():
            creation_form.save()
            messages.success(request, 'Регистрация завершена!')
            return redirect('loginUser')  
        else:
            messages.error(request, 'Проверьте данные на правильность!')
    else:
        creation_form = CreateUserForm()

    context = {'creation_form':creation_form}
    return render(request, 'core/register.html', context)


@login_required(login_url="loginUser")
def home(request):
    api_key = settings.API_KEY
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID='+ api_key +'&lang=ru'
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CityForm(request.POST)
            if form.is_valid():
                new_city = form.cleaned_data['name']
                city_user = City.objects.filter(user=request.user, name=new_city).count()

                if city_user == 0:
                    r = requests.get(url.format(new_city)).json()
                    if r['cod'] == 200:
                        urlCoord = 'https://geocode-maps.yandex.ru/1.x/?apikey=09ad4ed5-0e9c-4af7-9add-bd2bf3ff6953&geocode='+new_city+'&format=json'
                        instance = form.save(commit=False)
                        instance.created_by = request.user
                        instance.save()
                        form.save_m2m()
                        instance.user.add(request.user)
                        messages.success(request, 'Город успешно добавлен')
                        return redirect('home')   
                    else:
                        messages.error(request, 'Неверные координаты')
                        return redirect('home')
                else:
                    messages.error(request, 'Этот город уже добавлен')
                    return redirect('home')
            else:
                raise ValidationError("Invalid form!")
                messages.error("Неверная форма, убедитесь, что все данные верны!")
        else:
            form = CityForm()
        
    cities = City.objects.filter(user=request.user)
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'min_temperature': r['main']['temp_min'],
            'wind': r['wind']['speed'],
            'pressure': r['main']['pressure'],
            'humidity': r['main']['humidity'],
            'description': r['weather'][0]['description'],
            'icon':  r['weather'][0]['icon'],
            'id': city.pk,
        }
        print(city_weather)
        weather_data.append(city_weather)
    context = {
        'weather_data': weather_data, 
        'form': form,
    }
    return render(request, 'core/index.html', context)


@login_required(login_url="loginUser")
def delete(request, pk):
    
    City.objects.filter(user=request.user, pk=pk).delete()
    messages.success(request, 'Город успешно удален')
    return redirect('home')