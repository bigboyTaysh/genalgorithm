from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers
import genapp.modules as modules
from decimal import Decimal
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.template import RequestContext
import time


def index(request):
    return render(request, 'genapp/index.html')


def lab02(request):
    return render(request, 'genapp/lab02.html')


def lab03(request):
    return render(request, 'genapp/lab03.html')


def lab04(request):
    return render(request, 'genapp/lab04.html')


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
                                                 modules.get_individuals_array(range_a, range_b, precision, population, power))
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
            range_a, range_b, precision, population, power)
        randoms, selected_individuals = modules.selection_of_individuals(
            individuals, precision)
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
        probability_of_mutation = Decimal(
        request.POST['probability_of_mutation'])

        
        power = modules.power_of_2(range_a, range_b, precision)
        individuals = modules.get_individuals_array(
            range_a, range_b, precision, population, power)

        
        selected_individuals = modules.selection_of_individuals(
            individuals, precision)[1]
        
        modules.crossover(selected_individuals, crossover_probability,
                          range_a, range_b, precision, power)
        modules.mutation_of_individuals(
            selected_individuals, probability_of_mutation)

        new_population = []

        for individual in selected_individuals:
            new_population.append(modules.get_individual_from_binary(
                individual.mutant_population, range_a, range_b, precision, power))

        context = {
            'individuals': serializers.serialize("json", selected_individuals),
            'new_population': serializers.serialize("json", new_population)
        }

        return JsonResponse(context, status=200)
