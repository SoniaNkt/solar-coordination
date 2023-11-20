# coding: utf-8
import json
from random import gauss, randrange, randint, choice as random_choice

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from django.db import IntegrityError
from django.db.models import Count, Q

from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Participant, Condition
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
        return render(request, "solar_coordination_classic/index.html")
    except:
        raise Http404()

@login_required
def overview(request):
    print('overview')
    solar_values = [0,0,0,0,0,10,40,53,60,100,90,72,50,11,0,0,0,0,0]
    return render(request, "solar_coordination_classic/overview.html", {
        "solar_values": solar_values
        })
