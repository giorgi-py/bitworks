from django.urls import path
from .views import tools_view, check_port_view, dns_lookup_view, validate_host

urlpatterns = [
    path('tools/', tools_view, name='tools_url'),
    path('tools/check-port/', check_port_view, name='check_port'),
    path('tools/dns-lookup/', dns_lookup_view, name='dns_lookup_url'),
    path('tools/check-port/validate-host/', validate_host, name='validate_host'),
    # path('tools/check-port/port-input/', views.get_port_input, name='get_port_input'),
    # path('tools/check-port/history/', views.get_scan_history, name='get_scan_history')
]
