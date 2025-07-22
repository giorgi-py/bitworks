
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from user_agents import parse

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def parse_browser_from_user_agent(user_agent_string):
    user_agent = parse(user_agent_string)
    return f"{user_agent.browser.family} {user_agent.browser.version_string}"

def parse_os_from_user_agent(user_agent_string):
    user_agent = parse(user_agent_string)
    return f"{user_agent.os.family} {user_agent.os.version_string}"

def get_ip_info(ip):
    response = requests.get(f'https://ipapi.co/{ip}/json/')
    return response.json()


def home_view(request):
    x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    if x_forward:
        ip = x_forward.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    ip_detailed_info = get_ip_info(ip)
    user_info = {
        "city": ip_detailed_info.get('city', 'Unknown'),
        "region": ip_detailed_info.get('region', 'Unknown'),
        "country_name": ip_detailed_info.get('country_name', 'Unknown'),
        "org": ip_detailed_info.get('org', 'Unknown'),
        "asn": ip_detailed_info.get('asn', 'Unknown'),
        "browser": parse_browser_from_user_agent(user_agent) if user_agent else 'Unknown',
        "os": parse_os_from_user_agent(user_agent) if user_agent else 'Unknown',
    }
    return render(request, "home_nes.html", {
        'show_ip': ip,
        'user_agent': user_agent,
        'user_info': user_info,
        })

def services_view(request):
    return render(request, 'services.html')

def about_view(request):
    return render(request, 'about.html')

def contacts_view(r):
    return render(r, 'contacts.html')
