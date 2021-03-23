from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers
import genapp.modules as modules
from decimal import Decimal
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.template import RequestContext

# Create your views here.
def index(request):
    return render(request,'genapp/index.html')

def lab02(request):
    return render(request,'genapp/lab02.html')

def lab03(request):
    return render(request,'genapp/lab03.html')

def lab04(request):
    return render(request,'genapp/lab04.html')

def start(request):
    if request.is_ajax and request.method == "POST":
        range_a = Decimal(request.POST['range_a'])
        range_b = Decimal(request.POST['range_b'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])

        power = modules.power_of_2(range_a, range_b, precision)

        context = {
            'power': power,
            'individuals': serializers.serialize("json",
                                                 modules.get_individuals_array(range_a, range_b, precision, population))
        }

        return JsonResponse(context, status=200)

def selection(request):
    if request.is_ajax and request.method == "POST":
        range_a = Decimal(request.POST['range_a'])
        range_b = Decimal(request.POST['range_b'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])

        power = modules.power_of_2(range_a, range_b, precision)
        individuals = modules.get_individuals_array(
            range_a, range_b, precision, population)
        randoms, selected_individuals = modules.selection_of_individuals(individuals, precision, power)
        context = {
            'individuals': serializers.serialize("json", individuals),
            'randoms': randoms,
            'selected_individuals': serializers.serialize("json", selected_individuals)
        }

        return JsonResponse(context, status=200)

def crossover(request):
    if request.is_ajax and request.method == "POST":
        range_a = Decimal(request.POST['range_a'])
        range_b = Decimal(request.POST['range_b'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])
        crossover_probability = Decimal(request.POST['crossover_probability'])

        power = modules.power_of_2(range_a, range_b, precision)
        individuals = modules.get_individuals_array(
            range_a, range_b, precision, population, power)
        selected_individuals = modules.selection_of_individuals(individuals, precision)[1]
        childs = modules.crossover(selected_individuals, crossover_probability, range_a, range_b, precision, power)

        context = {
            'individuals': serializers.serialize("json", selected_individuals),
            'childs': serializers.serialize("json", childs)
        }

        return JsonResponse(context, status=200)