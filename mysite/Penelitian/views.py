# Penelitian/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import PenelitianDosen

def Penelitian(request):
    penelitian_list = PenelitianDosen.objects.all()
    paginator = Paginator(penelitian_list, 10)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    penelitian = paginator.get_page(page_number)

    return render(request, 'penelitian.html', {'penelitian': penelitian})
