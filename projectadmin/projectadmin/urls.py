"""projectadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf import settings #To use static files (.js, .css)
from django.conf.urls.static import static #To use static files (.js, .css)

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/timingcontrol/', permanent=True)),
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('timingcontrol/', include('timingcontrol.urls')),
]
urlpatterns += [
    path('', RedirectView.as_view(url='/timingcontrol/', permanent=True)),
]
#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#PARA LAS IMÁGENES
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
