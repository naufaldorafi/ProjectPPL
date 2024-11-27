# from django.shortcuts import render

# # Create your views here.
# def idePenelitian(request):
#     return render(request, 'idePenelitian.html')

from django.http import JsonResponse
from django.shortcuts import render
from Dosen.models import Dosen
import json

def idePenelitian(request):
    if request.method == 'POST':
        # Parsing data JSON dari permintaan POST
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Format data tidak valid. Pastikan data yang dikirim adalah JSON."
            })

        # Ambil nama dosen dari data input
        nama_dosen = data.get('nama_dosen', '').strip()
        if not nama_dosen:
            return JsonResponse({
                "status": "error",
                "message": "Nama dosen tidak boleh kosong. Silakan masukkan nama dosen."
            })

        # Cari dosen berdasarkan nama (case-insensitive)
        try:
            dosen = Dosen.objects.select_related(
                'Kepakaran_1', 'Kepakaran_2', 'Kepakaran_3'
            ).get(NamaDosen__iexact=nama_dosen)
            
            # Siapkan respons dengan data dosen
            response = {
                "status": "success",
                "message": f"Nama: {dosen.NamaDosen}\n"
                           f"NIDN: {dosen.NIDNDosen}\n"
                           f"Email: {dosen.EmailAkun}\n"
                           f"Kepakaran 1: {dosen.Kepakaran_1.nama if dosen.Kepakaran_1 else 'Tidak ada'}\n"
                           f"Kepakaran 2: {dosen.Kepakaran_2.nama if dosen.Kepakaran_2 else 'Tidak ada'}\n"
                           f"Kepakaran 3: {dosen.Kepakaran_3.nama if dosen.Kepakaran_3 else 'Tidak ada'}"
            }
        except Dosen.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Tidak ditemukan dosen dengan nama '{nama_dosen}'. Silakan coba nama lain."
            }
        except Exception as e:
            response = {
                "status": "error",
                "message": f"Terjadi kesalahan: {str(e)}"
            }
        
        return JsonResponse(response)

    # Jika bukan permintaan POST, render template
    return render(request, 'idePenelitian.html')