from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from genapp.modules import Modules

# Create your views here.
def index(request):
    template = loader.get_template('genapp/index.html')
    context = {
        'result': "Hello, world. You're at the genapp index."
    }
    return HttpResponse(template.render(context, request))

def start(request):
    if request.is_ajax and request.method == "POST":
        rel = request.POST['rel']
        ##rangeA = request.POST['rangeA']
        ##rangeB = request.POST['rangeB']
        ##precision = request.POST['precision']
        ##populationSize = request.POST['populationSize']

        ##Modules.random(rangeA, rangeB, precision)

        ##Modules.power_of_2(rangeA, rangeB, precision)    

        context = {
            'rel': rel
        }
        return JsonResponse(context, status=200)