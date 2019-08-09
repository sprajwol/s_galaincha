from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'mains/home.html')

def about(request):
    return render(request, 'mains/about.html', {'title': 'About'})