from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import genapp.modules
from decimal import Decimal

# Create your views here.
def index(request):
    template = loader.get_template('genapp/index.html')
    context = {
        'result': "Hello, world. You're at the genapp index."
    }
    return HttpResponse(template.render(context, request))

def start(request):
    if request.is_ajax and request.method == "POST":
        rangeA = Decimal(request.POST['rangeA'])
        rangeB = Decimal(request.POST['rangeB'])
        precision = int(request.POST['precision'])
        population = int(request.POST['population'])

        power = genapp.modules.power_of_2(rangeA, rangeB, precision)
 
        context = {
            'power': power,
            'individuals': genapp.modules.get_individual_array(rangeA, rangeB, precision, power, population)
        }
        
        return JsonResponse(context, status=200)