from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import PenelitianDosen, Dosen
import nltk
from rake_nltk import Rake
from collections import Counter
from django.core.paginator import Paginator


# Function to handle the "Penelitian" view
def Penelitian(request):
    search_query = request.GET.get('search', '')  # Ambil query pencarian

    # Filter berdasarkan pencarian (jika ada), jika tidak tampilkan semua
    if search_query:
        penelitian_list = PenelitianDosen.objects.filter(judul__icontains=search_query)
    else:
        penelitian_list = PenelitianDosen.objects.all()

    dosen_list = Dosen.objects.all()  # Ambil data dosen dari database

    # Konfigurasi Paginator (10 item per halaman)
    paginator = Paginator(penelitian_list, 10)  # Batasi 10 item per halaman

    # Ambil nomor halaman dari parameter GET
    page_number = request.GET.get("page")
    penelitian = paginator.get_page(page_number)  # Ambil halaman sesuai nomor

    # Render template dengan data pagination
    return render(request, 'penelitian.html', {
        'penelitian': penelitian,  # Data penelitian dengan pagination
        'dosen_list': dosen_list,  # Data dosen
        'search_query': search_query,  # Query pencarian
    })


# Function to handle the "Dosen List" view without pagination
def dosen_list(request):
    query = request.GET.get('q', '')  # Get the query parameter for search
    dosen_list = Dosen.objects.all()  # Retrieve all dosen objects

    if query:
        dosen_list = dosen_list.filter(NamaDosen__icontains=query)  # Filter by name if query exists

    return render(request, 'dosen.html', {
        'dosen_list': dosen_list,  # Pass the filtered list of dosen to the template
        'query': query,  # Pass the search query back to the template
    })

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

# Initialize RAKE for keyword extraction
rake = Rake()

# Function to categorize research and extract keywords
def categorize_research():
    research_data = PenelitianDosen.objects.filter(status='Active').values('scopus_id', 'judul', 'abstract')
    all_keywords = []  # List to store all extracted keywords

    for data in research_data:
        text = data["judul"] + " " + data["abstract"]  # Combine title and abstract for keyword extraction
        rake.extract_keywords_from_text(text)  # Extract keywords using RAKE
        keywords = rake.get_ranked_phrases()
        all_keywords.extend(keywords)  # Add extracted keywords to the list

    # Count occurrences of each keyword
    keyword_counts = Counter(all_keywords)

    # Format results as a sorted list of dictionaries
    result = sorted(
        [{'keyword': keyword, 'count': count} for keyword, count in keyword_counts.items()],
        key=lambda x: x['count'],
        reverse=True
    )
    return result

# API endpoint to run the categorize_research function and return results
@require_POST
def run_categorize_research(request):
    hasil = categorize_research()
    return JsonResponse({'hasil': hasil})
