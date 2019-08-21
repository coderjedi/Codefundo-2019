"""safevote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from vote import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^safevote/', views.oxford),
    url(r'^register/', views.register,name='register'),
    url(r'^login/', views.user_login,name='login'),
    url(r'vote/', views.vote,name='vote'),
    url(r'^logout/$', views.user_logout,name='logout'),
    url(r'^$', views.home,name='home'),

    url(r'^c_list/', views.c_list,name='c_list'),
    # url(r'^about/', views.about,name='about'),
    # url(r'^red/', views.voterred,name='red'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
