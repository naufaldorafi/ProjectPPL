# Penelitian/views.py
from django.shortcuts import render
from .models import PenelitianDosen  # Import model PenelitianDosen

def Penelitian(request):
    penelitian = PenelitianDosen.objects.all()  # Ambil semua data penelitian dari model PenelitianDosen
    return render(request, 'penelitian.html', {'penelitian': penelitian})
