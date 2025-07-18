from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def services_view(r):
    return render(r, 'services.html')

def network_services(r):
    return render(r, 'network_services.html')

def windows_server_view(r):
    return render(r, 'windows_server.html')

