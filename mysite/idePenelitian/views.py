import http.client
import json
from django.http import JsonResponse
from django.shortcuts import render
from Dosen.models import Dosen
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def idePenelitian(request):
    if request.method == 'POST':
        try:
            # Memuat data dari permintaan POST
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Format data tidak valid. Pastikan data yang dikirim adalah JSON."
            })

        # Validasi input nama dosen
        nama_dosen = data.get('nama_dosen', '').strip()
        if not nama_dosen:
            return JsonResponse({
                "status": "error",
                "message": "Nama dosen tidak boleh kosong. Silakan masukkan nama dosen."
            })

        # Mencari dosen berdasarkan nama
        dosen_list = Dosen.objects.filter(NamaDosen__icontains=nama_dosen)

        if not dosen_list.exists():
            return JsonResponse({
                "status": "error",
                "message": f"Tidak ditemukan dosen dengan nama '{nama_dosen}'. Silakan coba nama lain."
            })

        ide_penelitian_list = []
        for dosen in dosen_list:
            # Ambil data kepakaran dosen
            kepakaran = [
                dosen.Kepakaran_1.nama if dosen.Kepakaran_1 else None,
                dosen.Kepakaran_2.nama if dosen.Kepakaran_2 else None,
                dosen.Kepakaran_3.nama if dosen.Kepakaran_3 else None,
            ]
            kepakaran = [k for k in kepakaran if k]  # Filter None values

            if not kepakaran:
                ide_penelitian_list.append({
                    "nama_dosen": dosen.NamaDosen,
                    "kepakaran": [],
                    "ide_penelitian": "Tidak ada kepakaran yang terdaftar untuk dosen ini."
                })
                continue

            # Header dan payload untuk RapidAPI
            headers = {
                "x-rapidapi-key": "6d79d2d3dbmsh3ac71c987c554bfp1c3c36jsn2627c332c7e4",
                "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
                "Content-Type": "application/json"
            }
            payload = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"Buatkan 3 ide penelitian skripsi berdasarkan kepakaran berikut: {', '.join(kepakaran)}. Dengan jelas singkat padat, langsung pada jawabannya, tanpa di bold, tidak perlu menjelaskan penelitiannya, langsung judul saja"
                        )
                    }
                ],
                "web_access": False
            })

            try:
                # Membuka koneksi HTTP
                conn = http.client.HTTPSConnection("chatgpt-42.p.rapidapi.com")

                # Mengirim permintaan POST
                conn.request("POST", "/gpt4", payload, headers)

                # Mendapatkan respons
                response = conn.getresponse()
                response_data = response.read().decode('utf-8')
                conn.close()

                # Log untuk memeriksa respons dari API
                print("API Response Data:", response_data)

                if response.status == 200:
                    api_response = json.loads(response_data)
                    result = api_response.get('result', '')
                    if result:
                        ide_penelitian_list.append({
                            "nama_dosen": dosen.NamaDosen,
                            "kepakaran": kepakaran,
                            "ide_penelitian": result
                        })
                    else:
                        ide_penelitian_list.append({
                            "nama_dosen": dosen.NamaDosen,
                            "kepakaran": kepakaran,
                            "ide_penelitian": "Tidak ada ide penelitian yang dihasilkan."
                        })
                else:
                    ide_penelitian_list.append({
                        "nama_dosen": dosen.NamaDosen,
                        "kepakaran": kepakaran,
                        "ide_penelitian": f"Permintaan ke API gagal dengan status {response.status}"
                    })

            except Exception as e:
                ide_penelitian_list.append({
                    "nama_dosen": dosen.NamaDosen,
                    "kepakaran": kepakaran,
                    "ide_penelitian": f"Terjadi kesalahan saat menghubungi API: {str(e)}"
                })

        # Kirim data dalam format JSON
        return JsonResponse({
            "status": "success",
            "ide_penelitian": ide_penelitian_list
        })

    # Jika GET, hanya menampilkan form pencarian
    return render(request, 'idePenelitian.html')