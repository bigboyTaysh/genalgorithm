from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers
import genapp.modules as modules
from decimal import Decimal

# Create your views here.


def index(request):
    template = loader.get_template('genapp/index.html')
    return HttpResponse(template.render())


def lab02(request):
    template = loader.get_template('genapp/lab02.html')
    return HttpResponse(template.render())


def lab03(request):
    template = loader.get_template('genapp/lab03.html')
    return HttpResponse(template.render())


def start(request):
    if request.is_ajax and request.method == "POST":
        rangeA = Decimal(request.POST['rangeA'])
        rangeB = Decimal(request.POST['rangeB'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])

        power = modules.power_of_2(rangeA, rangeB, precision)

        context = {
            'power': power,
            'individuals': serializers.serialize("json",
                                                 modules.get_individuals_array(rangeA, rangeB, precision, power, population))
        }

        return JsonResponse(context, status=200)


def selection(request):
    if request.is_ajax and request.method == "POST":
        rangeA = Decimal(request.POST['rangeA'])
        rangeB = Decimal(request.POST['rangeB'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])
        power = modules.power_of_2(rangeA, rangeB, precision)

        individuals = modules.get_individuals_array(
            rangeA, rangeB, precision, power, population)

        context = {
            'individuals': serializers.serialize("json",
                                                 modules.selection_of_individuals(individuals))
        }
        return JsonResponse(context, status=200)
