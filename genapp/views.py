from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('genapp/index.html')
    context = {
        'result': "Hello, world. You're at the genapp index."
    }
    return HttpResponse(template.render(context, request))

def start(request):
    rangeA = request.POST['rangeA']
    rangeB = request.POST['rangeB']
    template = loader.get_template('genapp/index.html')
    context = {
        'rangeA': rangeA,
        'rangeB': rangeB
    }
    return HttpResponse(template.render(context, request))