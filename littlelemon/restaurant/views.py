from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .forms import BookingForm
from .models import Booking, Menu
import json


def index(request):
    return render(request, 'index.html')


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')


def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/')  # Redireciona após o sucesso
    context = {'form': form}
    return render(request, 'book.html', context)

def reservations(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    return HttpResponse(booking_json, content_type='application/json')

# @csrf_exempt
# def bookings(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         exists = Booking.objects.filter(
#             reservation_date=data['reservation_date'],
#             reservation_slot=data['reservation_slot']
#         ).exists()
#         if not exists:
#             Booking.objects.create(
#                 first_name=data['first_name'],
#                 reservation_date=data['reservation_date'],
#                 reservation_slot=data['reservation_slot']
#             )
#             return HttpResponse('{"success":1}', content_type='application/json')
#         else:
#             return HttpResponse('{"error": "Slot not available"}', content_type='application/json')

#     date = request.GET.get('date', datetime.today().date())
#     bookings = Booking.objects.filter(reservation_date=date)
#     booking_json = serializers.serialize('json', bookings)
#     return HttpResponse(booking_json, content_type='application/json')
