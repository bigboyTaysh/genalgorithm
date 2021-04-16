from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core import serializers
from django.conf import settings
import genapp.modules as modules
from decimal import Decimal
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.template import RequestContext
import time
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
from django.http import Http404
from django.shortcuts import redirect
import pickle

def index(request):
    return render(request, 'genapp/index.html')


def lab02(request):
    return render(request, 'genapp/lab02.html')


def lab03(request):
    return render(request, 'genapp/lab03.html')


def lab04(request):
    return render(request, 'genapp/lab04.html')


def lab05(request):
    return render(request, 'genapp/lab05.html')


def start(request):
    if request.is_ajax and request.method == "POST":
        range_a = float(request.POST['range_a'])
        range_b = float(request.POST['range_b'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])

        power = modules.power_of_2(range_a, range_b, precision)
        individuals = modules.get_individuals_array(range_a, range_b, precision, population, power)
        context = {
            'power': power,
            'individuals': json.dumps([individual.__dict__ for individual in individuals])
        }

        return JsonResponse(context, status=200)


def selection(request):
    if request.is_ajax and request.method == "POST":
        range_a = float(request.POST['range_a'])
        range_b = float(request.POST['range_b'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])

        power = modules.power_of_2(range_a, range_b, precision)
        individuals = modules.get_individuals_array(
            range_a, range_b, precision, population, power)
        selected_individuals = modules.selection_of_individuals(
            individuals, precision)

        context = {
            'individuals': json.dumps([individual.__dict__ for individual in individuals]),
            'selected_individuals': json.dumps([individual.__dict__ for individual in selected_individuals]),
        }

        return JsonResponse(context, status=200)


def crossover(request):
    if request.is_ajax and request.method == "POST":
        range_a = float(request.POST['range_a'])
        range_b = float(request.POST['range_b'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])
        crossover_probability = float(request.POST['crossover_probability'])
        mutation_probability = float(
            request.POST['mutation_probability'])

        power = modules.power_of_2(range_a, range_b, precision)

        individuals = modules.get_individuals_array(
            range_a, range_b, precision, population, power)

        selected_individuals = modules.selection_of_individuals(
            individuals, precision)

        modules.crossover(selected_individuals, crossover_probability, power)
        modules.mutation(
            selected_individuals, mutation_probability, power)

        new_population = []

        for individual in selected_individuals:
            new_population.append(modules.get_individual_from_binary(
                individual.mutant_population, range_a, range_b, precision, power))

        print(new_population[0].mutant_population)

        context = {
            'individuals': json.dumps([individual.__dict__ for individual in selected_individuals.tolist()]),
            'new_population': json.dumps([individual.__dict__ for individual in new_population])
        }

        return JsonResponse(context, status=200)


def evolution(request):
    if request.is_ajax and request.method == "POST":
        range_a = float(request.POST['range_a'])
        range_b = float(request.POST['range_b'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])
        generations_number = int(request.POST['generations'])
        crossover_probability = float(request.POST['crossover_probability'])
        mutation_probability = float(
            request.POST['mutation_probability'])
        elite_number = int(request.POST['elite'])

        generations = modules.evolution(range_a, range_b, precision, population, generations_number, crossover_probability, mutation_probability, elite_number, True)
         
        results = []
        last_generation = generations[-1]
        data_for_chart =[]

        for index in range(0, population):
            if not any(result['real'] == last_generation.individuals[index].real for result in results):
                results.append({'real': last_generation.individuals[index].real,
                    'bin': last_generation.individuals[index].binary,
                    'fx': last_generation.individuals[index].fx,
                    'percent': round(sum(individual.real == last_generation.individuals[index].real for individual in last_generation.individuals) / population * 100, 2)})

        for generation in generations:
            data_for_chart.append({'fmin': generation.fmin, 'favg': generation.favg, 'fmax': generation.fmax})

        context = {
            'last_generation': sorted(results, key=lambda x: x['percent'], reverse=True),
            'data_for_chart': data_for_chart
        }

        return JsonResponse(context, status=200)


def test(request):
    if request.is_ajax and request.method == "POST":
        tests_number = int(request.POST['tests_number'])
        precision = int(request.POST['precision'])

        tests_list = sorted(modules.test(tests_number, precision), key=lambda x: (x.favg, x.fmax), reverse=True)

        context = {
            'test': json.dumps([test.__dict__ for test in tests_list]),
        }
        
        return JsonResponse(context, status=200)


def download(request, path):
    print(os.path.join(settings.STATIC_ROOT, path))
    file_path = os.path.join(settings.STATIC_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return redirect('lab05')