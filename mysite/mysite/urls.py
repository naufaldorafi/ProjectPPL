"""
URL configuration for mysite project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from idePenelitian.views import idePenelitian
from Penelitian.views import Penelitian
from Dosen import views as dosen_views
from detailDosen.views import detailDosen
from login.views import register
from Dosen import views
from Dosen.views import fetch_scopus_data_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ide-penelitian/', idePenelitian, name='ide-penelitian'),
    path('', idePenelitian, name='ide-penelitian'),
    path('penelitian/', Penelitian, name='penelitian'),
    path('dosen/', dosen_views.dosen_list, name='dosen'),
    path('detail/<int:id>/', detailDosen, name='detail-dosen'),
    path('register/', register, name='register'),
    path('', include("django.contrib.auth.urls")),
    path('fetch-scopus-data/', views.fetch_scopus_data_view, name='fetch_scopus_data')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
