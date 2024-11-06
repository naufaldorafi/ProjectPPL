# dosen/views.py
from django.shortcuts import render
import requests
import time
from django.http import JsonResponse
from Penelitian.models import PenelitianDosen, TopikPenelitian  # Import model dari app penelitian

def Dosen(request):
    return render(request, 'dosen.html')

# def fetch_scopus_data_view(request):
#     API_KEY = '8d1c5ea6ed9e64cfd2dce678c4ac72df'
#     author_ids = [
#     '57210671389',
#     '57210823615',
#     '57212507646',
#     '56426242200',
#     '57222305409',
#     '57202163318',
#     '56397160600',
#     '57213276294',
#     '56592788400',
#     '57094026700',
#     '57202941647',
#     '55613484700',
#     '57204975149',
#     '57204974337',
#     '57209977071',
#     '57195415503'
# ]
#     headers = {
#         'X-ELS-APIKey': API_KEY,
#         'Accept': 'application/json'
#     }
    
#     results = []
#     for author_id in author_ids:
#         url = f'https://api.elsevier.com/content/search/scopus?query=AU-ID({author_id})'
#         response = requests.get(url, headers=headers)
        
#         if response.status_code == 200:
#             data = response.json()
#             print("Data yang diambil dari API:", data)  # Debugging
            
#             for item in data['search-results']['entry']:
#                 title = item.get("dc:title", "N/A")
#                 abstract = item.get("dc:abstract") or item.get("dc:description", "N/A")
#                 publication_date = item.get("prism:coverDate", None)
#                 publication_type = item.get("subtype", "N/A")[0] if item.get("subtype") else None
#                 source = item.get("prism:publicationName", "N/A")

#                 penelitian_dosen = PenelitianDosen(
#                     judul=title,
#                     abstract=abstract,
#                     tanggal_publikasi=publication_date,
#                     tipe_publikasi=publication_type,
#                     sumber=source,
#                     # Anda bisa menambahkan topik penelitian di sini jika diperlukan
#                 )
#                 penelitian_dosen.save()  # Simpan ke database
#                 results.append({
#                     "title": title,
#                     "abstract": abstract,
#                     "publication_date": publication_date,
#                     "publication_type": publication_type,
#                     "source": source
#                 })
#         else:
#             results.append({"author_id": author_id, "error": response.status_code})
        
#         time.sleep(1)
    
#     return JsonResponse({"data": results})

def fetch_scopus_data_view(request):
    API_KEY = '8d1c5ea6ed9e64cfd2dce678c4ac72df'
    author_ids = [
        '57210671389', '57210823615', '57212507646', '56426242200', '57222305409',
        '57202163318', '56397160600', '57213276294', '56592788400', '57094026700',
        '57202941647', '55613484700', '57204975149', '57204974337', '57209977071', 
        '57195415503'
    ]
    headers = {
        'X-ELS-APIKey': API_KEY,
        'Accept': 'application/json'
    }
    
    results = []
    for author_id in author_ids:
        url = f'https://api.elsevier.com/content/search/scopus?query=AU-ID({author_id})'
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for item in data['search-results']['entry']:
                title = item.get("dc:title", "N/A")
                scopus_id = item.get("dc:identifier", "").split(":")[-1]  # Ambil scopus_id
                
                # Ambil abstrak menggunakan Abstract Retrieval API
                abstract = "Abstract not available"
                if scopus_id:
                    abstract_url = f'https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}'
                    abstract_response = requests.get(abstract_url, headers=headers)
                    if abstract_response.status_code == 200:
                        abstract_data = abstract_response.json()
                        abstract = abstract_data.get("abstracts-retrieval-response", {}).get("coredata", {}).get("dc:description", "Abstract not available")
                
                publication_date = item.get("prism:coverDate", None)
                publication_type = item.get("subtype", "N/A")[0] if item.get("subtype") else None
                source = item.get("prism:publicationName", "N/A")

                # Gunakan get_or_create untuk menghindari duplikasi
                penelitian_dosen, created = PenelitianDosen.objects.get_or_create(
                    scopus_id=scopus_id,  # Menggunakan scopus_id untuk mencari
                    defaults={
                        'judul': title,
                        'abstract': abstract,
                        'tanggal_publikasi': publication_date,
                        'tipe_publikasi': publication_type,
                        'sumber': source,
                        'status': "Active"  # Atau status lain sesuai kebutuhan
                    }
                )
                if created:
                    results.append({
                        "scopus_id": scopus_id,
                        "title": title,
                        "abstract": abstract,
                        "publication_date": publication_date,
                        "publication_type": publication_type,
                        "source": source,
                        "message": "New entry created."
                    })
                else:
                    results.append({
                        "scopus_id": scopus_id,
                        "title": title,
                        "abstract": abstract,
                        "publication_date": publication_date,
                        "publication_type": publication_type,
                        "source": source,
                        "message": "Entry already exists."
                    })
        else:
            results.append({"author_id": author_id, "error": response.status_code})
        
        # Penundaan untuk menghindari pembatasan API rate limit
        time.sleep(1)
    
    return JsonResponse({"data": results})