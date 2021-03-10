from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from genapp.modules import power_of_2, real_to_int, bin_to_int
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
        real = Decimal(request.POST['real'])
        binary = Decimal(request.POST['bin'])
        rangeA = Decimal(request.POST['rangeA'])
        rangeB = Decimal(request.POST['rangeB'])
        precision = Decimal(request.POST['precision'])
        precision = Decimal(request.POST['precision'])

        context = {
            'power': power_of_2(rangeA, rangeB, precision),
            'real': real_to_int(real, rangeA, rangeB, precision),
            'bin': bin_to_int(binary)
        }
        return JsonResponse(context, status=200)