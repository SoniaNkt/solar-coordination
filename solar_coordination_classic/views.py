# coding: utf-8
import json
import re
from decimal import Decimal
from random import gauss, randrange, randint, choice as random_choice
from collections import defaultdict

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import datetime
from django.db import IntegrityError
from django.db.models import Count, Q, Sum, F, Min, Max
from django.db.models.functions import Trunc

from .models import Participant, Condition, SolarGeneration, SolarGenerationProfile, Booking, EnergyPricing, ComfortProfile, ComfortCostSlot
from .djutils import to_dict

# Create your views here.


def welcome_page(request):
    return render(request, 'welcome.html')


@csrf_exempt
@require_POST
def participants_view(request):
    username = request.POST['username']
    is_test_user = False
    if username == "TEST":
        username = "TEST_USER__{}".format(datetime.strftime(datetime.now(), '%Y_%m_%d__%H_%M_%S'))
        # is_test_user = True

    try:
        user = User.objects.create_user(username=username)
        user.save()
        print("Created user:", repr(user))
    except IntegrityError:
        error = {
            "username": [{"message": "This field is duplicate.", "code": "duplicate"}]
            }
        data = json.dumps(error)
        return HttpResponseBadRequest(data, content_type='application/json')

    participant = Participant()
    participant.user = user
    # participant.created_for_testing = is_test_user

    # assign condition
    # sort by number of runs/participants
    # filter out TEST participants from this count
    all_conditions = Condition.objects.filter(active=True
        ).annotate(n_participants=Count('participant',
            exclude=Q(participant__user__username__startswith='TEST_USER__'))
        ).order_by('n_participants')
    
    # take the min value
    min_participants = all_conditions[0].n_participants
    # get all TaskList objects which have the min value of completed tasks..
    min_conditions = all_conditions.filter(n_participants=min_participants)
    no_conditions = min_conditions.count()
    # ..and randomly pick one of them
    index = randint(0, no_conditions-1)
    participant.condition = min_conditions[index]
    # all_conditions = Condition.objects.filter(active=True
    #     ).annotate(n_participants=Count('participant')
    #     ).order_by('n_participants')
    # participant.condition = all_conditions[0]

    participant.save()

    login(request, user)

    #data = json.dumps(to_dict(participant, transverse=True))
    data = json.dumps(to_dict(user, transverse=False))
    return HttpResponse(data, content_type='application/json')


@login_required
def index(request):
    try:
        return render(request, "index.html")
    except:
        raise Http404()


@login_required
def overview(request):
    current_user = request.user
    participant = Participant.objects.get(user=current_user)
    group_size = participant.condition.group_size

    hourly_user_booking_values_dict = fetch_cumulative_hourly_user_bookings(current_user)
    solar_values_dict = fetch_solar_values()

    solar_spend_list = []
    for hour, booked_amount in hourly_user_booking_values_dict.items():
        solar_amount = solar_values_dict.get(hour)
        solar_spend_list.append({'hour': hour, 'amount': (int(solar_amount)/group_size) - float(booked_amount)}) # if positive they used their portion if -ve they borrowed from their neighbors

    truncated_created_at = Trunc('created_at', 'second')
    user_bookings = (
        Booking.objects
        .filter(user=current_user)
        .annotate(truncated_created_at=truncated_created_at)
        .values('name', 'truncated_created_at')
        .annotate(
            total_amount=Sum('amount'),
            min_hour=Min('hour'),
            max_hour=Max('hour')
        )
        .order_by('truncated_created_at')
    )

    consolidated_bookings = list(user_bookings)
    total_electricity_savings = calculate_electricity_savings(solar_spend_list)
    reward = calculate_reward(participant.comfort_profile, hourly_user_booking_values_dict)

    return render(request, 'overview.html', {'consolidated_bookings': consolidated_bookings, 'total_electricity_savings': total_electricity_savings, 'reward': reward})


def fetch_cumulative_hourly_user_bookings(current_user):
    user_booking_values = (
        Booking.objects
        .filter(user=current_user)
        .values('hour')
        .annotate(cumulative_booking_amount=Sum('amount'))
        .order_by('hour')
    )  
    booking_values_dict = {str(item['hour']): item['cumulative_booking_amount'] for item in user_booking_values}

    return booking_values_dict


def fetch_solar_values():
    default_profile = SolarGenerationProfile.objects.get(name="Sunny Autumn Day")  
    solar_values = SolarGeneration.objects.filter(solar_generation_profile=default_profile).order_by('hour').only('hour', 'amount')
    solar_values_dict = {str(item.hour): item.amount for item in solar_values}

    return solar_values_dict


def calculate_electricity_savings(solar_spend_list):
    energy_pricing = EnergyPricing.objects.get(name='UK Energy Pricing', active=True)

    for entry in solar_spend_list:
        amount = entry['amount']

        # if positive they used their portion if -ve they borrowed from their neighbors
        if amount > 0: 
            entry['electricity_savings'] = amount*float(energy_pricing.import_price) # what they would have pulled from the grid
        elif amount < 0:
            entry['electricity_savings'] = (abs(amount)*float(energy_pricing.import_price)) - (abs(amount)*float(energy_pricing.export_price)) # what they would have pulled from the grid minus what they pulled from their neighbors
        else:
            entry['electricity_savings'] = 0

    total_electricity_savings = format(sum(entry['electricity_savings'] for entry in solar_spend_list), '.2f')

    return total_electricity_savings

def calculate_reward(user_comfort_profile, hourly_user_booking_values_dict):
    comfort_cost_values = ComfortCostSlot.objects.filter(comfort_profile=user_comfort_profile).order_by('hour').only('hour', 'cost')
    comfort_cost_values_dict = {str(item.hour): item.cost for item in comfort_cost_values}

    reward = []
    for hour, booked_amount in hourly_user_booking_values_dict.items():
        hourly_cost = comfort_cost_values_dict.get(hour, 0)
        reward.append({'hour': hour, 'cost': float(booked_amount)*float(hourly_cost)})

    total_reward = format(sum(item['cost'] for item in reward), '.2f')
    return total_reward

@login_required
def fetch_solar_and_booked_values(request):
    booking_values = (
        Booking.objects
        .values('hour')
        .annotate(cumulative_booking_amount=Sum('amount'))
        .order_by('hour')
    )   
    booking_values_dict = {str(item['hour']): item['cumulative_booking_amount'] for item in booking_values}
    solar_values_dict = fetch_solar_values()

    solar_values_list = []
    for hour, solar_amount in solar_values_dict.items():
        booked_amount = booking_values_dict.get(hour, 0)  # Get the cumulative booked amount or default to 0
        solar_values_list.append({'hour': hour, 'amount': [int(solar_amount), booked_amount]})

    return JsonResponse({'data': solar_values_list})


@csrf_exempt
@login_required
def create_booking(request):
    if request.method == 'POST':
        hour = int(request.POST.get('hour'))
        amount = int(request.POST.get('amount'))
        name = request.POST.get('name')
        user = request.user 

        duration = int(re.findall(r'\d+', name)[0])
        hourly_consumption = amount/duration

        for i in range(duration):
            booking = Booking.objects.create(
                user=user,
                hour=hour,
                name=name,
                amount=hourly_consumption,
            )
            booking.save()
            hour += 1

        return redirect('overview')

    response_data = {'error': 'Unsupported method'}
    return JsonResponse(response_data, status=405)