from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from genapp.modules import power_of_2
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
        ##rel = Decimal(request.POST['rel'])
        rangeA = Decimal(request.POST['rangeA'])
        rangeB = Decimal(request.POST['rangeB'])
        precision = Decimal(request.POST['precision'])
        ##populationSize = request.POST['populationSize']

        ##Modules.random(rangeA, rangeB, precision)

        ##Modules.power_of_2(rangeA, rangeB, precision)    

        context = {
            'rel': power_of_2(rangeA, rangeB, precision)
        }
        return JsonResponse(context, status=200)