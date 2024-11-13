from django.shortcuts import render, get_object_or_404
from Dosen.models import Dosen
from Penelitian.models import PenelitianDosen

# Create your views here.
def detailDosen(request, id):
    dosen = get_object_or_404(Dosen, id=id)
    penelitian_dosen = PenelitianDosen.objects.filter(dosen=dosen)
    
    # Menghitung jumlah penelitian
    jumlah_penelitian = penelitian_dosen.count()
    
    return render(request, 'detaildosen.html', {
        'dosen': dosen,
        'penelitian_dosen': penelitian_dosen,
        'jumlah_penelitian': jumlah_penelitian  # Kirimkan jumlah penelitian ke template
    })