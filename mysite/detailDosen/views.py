from django.shortcuts import render, get_object_or_404
from Dosen.models import Dosen
from Penelitian.models import PenelitianDosen

# Create your views here.
def detailDosen(request, id):
    dosen = Dosen.objects.get(id=id)
    penelitian_dosen = PenelitianDosen.objects.filter(dosen=dosen)
    
    return render(request, 'detaildosen.html', {'dosen': dosen, 'penelitian_dosen': penelitian_dosen})