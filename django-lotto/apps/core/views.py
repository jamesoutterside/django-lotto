from django.shortcuts import render

def index(request):
    bag = {}

    return render(request, 'core/index.html', bag)