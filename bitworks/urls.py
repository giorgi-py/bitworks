"""
URL configuration for bitworks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns, set_language
from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path("i18n/setlang/", set_language, name="set_language"),
    path('', views.home_view, name="homeurl"),
    path('contacts/', views.contacts_view, name="contacts_url"),
    # path('services/', views.services_view, name="servicesurl"),
    # path('services/services-stack/', views.services_stack, name="servicesstackurl"),
    path ('', include('services.urls')),
    path ('', include('tools.urls')),
    path('about/', views.about_view, name="abouturl"),
)
urlpatterns += [
    path('i18n', include('django.conf.urls.i18n'))
]