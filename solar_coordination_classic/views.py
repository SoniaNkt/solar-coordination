from django.shortcuts import render
from django.http import Http404
# Create your views here.

def index(request):
    try:
        return render(request, "solar_coordination_classic/index.html")
    except:
        raise Http404()

def overview(request):
    try:
        solar_values = [0,0,0,0,0,10,40,53,60,100,90,72,50,11,0,0,0,0,0]
        return render(request, "solar_coordination_classic/overview.html", {
            "solar_values": solar_values
            })
    except:
        raise Http404()