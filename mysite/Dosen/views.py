# dosen/views.py
from django.shortcuts import render
import requests
import time
from django.http import JsonResponse
from Penelitian.models import PenelitianDosen, TopikPenelitian  # Import model dari app penelitian
from .models import Dosen
from django.conf import settings
from django.core.paginator import Paginator

# def Dosen(request):
    # return render(request, 'dosen.html')

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

def dosen_list(request):
    dosen_list = Dosen.objects.all()  # Mengambil semua data dosen
    return render(request, 'dosen.html', {'dosen_list': dosen_list})

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
        page = 1  # Start from page 1
        while True:  # Loop through pages for pagination
            url = f'https://api.elsevier.com/content/search/scopus?query=AU-ID({author_id})&start={(page - 1) * 25}&count=25'
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check if 'entry' exists in the response
                    if 'entry' not in data['search-results']:
                        results.append({"author_id": author_id, "message": "No entries found."})
                        break  # No more pages with data

                    # Process the 'entry' data
                    for item in data['search-results']['entry']:
                        title = item.get("dc:title", "N/A")
                        scopus_id = item.get("dc:identifier", "").split(":")[-1]

                        # Only fetch abstract if scopus_id exists
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

                        # Use get_or_create to avoid duplicate scopus_id
                        penelitian_dosen, created = PenelitianDosen.objects.get_or_create(
                            scopus_id=scopus_id,  # Ensure scopus_id uniqueness
                            defaults={
                                'author_id': author_id,
                                'judul': title,
                                'abstract': abstract,
                                'tanggal_publikasi': publication_date,
                                'tipe_publikasi': publication_type,
                                'sumber': source,
                            }
                        )

                        if created:
                            results.append({
                                "author_id": author_id,
                                "scopus_id": scopus_id,
                                "title": title,
                                "abstract": abstract,
                                "publication_date": publication_date,
                                "publication_type": publication_type,
                                "source": source,
                            })
                        else:
                            results.append({
                                "author_id": author_id,
                                "scopus_id": scopus_id,
                                "title": title,
                                "abstract": abstract,
                                "publication_date": publication_date,
                                "publication_type": publication_type,
                                "source": source,
                            })

                except KeyError as e:
                    results.append({"author_id": author_id, "error": f"Missing key: {str(e)}"})
            else:
                results.append({"author_id": author_id, "error": response.status_code})

            # Increment page number for pagination
            page += 1

            # Break if no more results are found in the current page
            if len(data['search-results'].get('entry', [])) < 25:
                break

            # Sleep to avoid rate limiting
            time.sleep(1)

    return JsonResponse({"data": results})
# Tempatkan API key Anda di sini
SCOPUS_API_KEY = '8d1c5ea6ed9e64cfd2dce678c4ac72df'

def fetch_author_profile(request):
    # Daftar author_id yang didaftarkan secara manual
    author_ids = ['57210671389', '57210823615', '57212507646', '56426242200', '57222305409',
        '57202163318', '56397160600', '57213276294', '56592788400', '57094026700',
        '57202941647', '55613484700', '57204975149', '57204974337', '57209977071', 
        '57195415503']

    author_profiles = []

    for author_id in author_ids:
        # URL API Scopus untuk mengambil profil penulis berdasarkan author_id
        url = f"https://api.elsevier.com/content/author/author_id/{author_id}"
        
        # Mengirim permintaan GET ke API Scopus
        response = requests.get(url, headers={
            "Accept": "application/json",
            "X-ELS-APIKey": SCOPUS_API_KEY
        })

        # Memeriksa status respons
        if response.status_code == 200:
            data = response.json()

            # Mengambil data profil penulis yang relevan
            subject_areas = [
                area.get("$", "N/A") 
                for area in data.get("author-retrieval-response", [{}])[0].get("subject-areas", {}).get("subject-area", [])
            ]

            # Menyimpan subject areas ke model TopikPenelitian
            for subject_area in subject_areas:
                if subject_area != "N/A":  # Abaikan jika nilai tidak valid
                    # Periksa apakah subject area sudah ada di database
                    if not TopikPenelitian.objects.filter(nama=subject_area).exists():
                        TopikPenelitian.objects.create(nama=subject_area)

            # Menambahkan data penulis ke author_profiles (opsional untuk dikembalikan dalam respons)
            author_profile = {
                "author_id": author_id,
                "author_name": data.get("author-retrieval-response", [{}])[0].get("preferred-name", {}).get("given-name", "") + " " +
                               data.get("author-retrieval-response", [{}])[0].get("preferred-name", {}).get("surname", ""),
                "document_count": data.get("author-retrieval-response", [{}])[0].get("coredata", {}).get("document-count", "N/A"),
                "citation_count": data.get("author-retrieval-response", [{}])[0].get("coredata", {}).get("citation-count", "N/A"),
                "affiliation": data.get("author-retrieval-response", [{}])[0].get("affiliation-current", {}).get("affiliation-name", "N/A"),
                "subject_areas": subject_areas
            }
            author_profiles.append(author_profile)
        else:
            author_profiles.append({
                "author_id": author_id,
                "error": f"Permintaan gagal dengan status {response.status_code}: {response.text}"
            })
        # Hindari terlalu banyak permintaan ke API dalam waktu singkat
        time.sleep(1)

    return JsonResponse({"authors": author_profiles})

def dosen_list(request):
    dosen_list = Dosen.objects.all()
    paginator = Paginator(dosen_list, 8)  # Batasi 8 dosen per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Dosen/dosen.html', {'page_obj': page_obj})