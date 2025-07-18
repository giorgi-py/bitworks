from django.urls import path
from .views import services_view, network_services, windows_server_view

urlpatterns = [
    path('services/', services_view, name='servicesurl'),
    path('services/network-services/', network_services, name='network_services'),
    path('services/windows-server/', windows_server_view, name='windows_server_url'),
]
