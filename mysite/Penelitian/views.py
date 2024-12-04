from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import PenelitianDosen, Dosen
# import nltk
# from rake_nltk import Rake
from collections import Counter
from django.core.paginator import Paginator
from django.db.models import Q
from urllib.parse import urlencode

# Function to handle the "Penelitian" view
def Penelitian(request):
    search_query = request.GET.get('search', '')
    tahun_filter = request.GET.get("tahun", None)
    tahun_start = request.GET.get("tahun_start", None)
    tahun_end = request.GET.get("tahun_end", None)
    dosen_filter = request.GET.get("dosen", None)
    bidang_filter = request.GET.get("bidang", None)
    
    penelitian_list = PenelitianDosen.objects.all()
    dosen_list = Dosen.objects.all()
    subject_area_list = set()

    # Search Penelitian
    if search_query:
        penelitian_list = PenelitianDosen.objects.filter(judul__icontains=search_query)
    else:
        penelitian_list = PenelitianDosen.objects.all()

    # Filterisasi Tahun
    if tahun_filter:
        penelitian_list = penelitian_list.filter(tanggal_publikasi__year=tahun_filter)
    
    if tahun_start and tahun_end:
        penelitian_list = penelitian_list.filter(
            tanggal_publikasi__year__gte=tahun_start,
            tanggal_publikasi__year__lte=tahun_end
        ).order_by('tanggal_publikasi')

    # Filterisasi Bidang
    for dosen in dosen_list:
        if dosen.Kepakaran_1:
            subject_area_list.add(dosen.Kepakaran_1.nama)
        if dosen.Kepakaran_2:
            subject_area_list.add(dosen.Kepakaran_2.nama)
        if dosen.Kepakaran_3:
            subject_area_list.add(dosen.Kepakaran_3.nama)
    
    bidang_filter = request.GET.get("bidang", None)

    if bidang_filter:
        penelitian_list = penelitian_list.filter(
            Q(dosen__Kepakaran_1__nama=bidang_filter) |
            Q(dosen__Kepakaran_2__nama=bidang_filter) |
            Q(dosen__Kepakaran_3__nama=bidang_filter)
        )
    if dosen_filter:
        penelitian_list = penelitian_list.filter(dosen__NamaDosen=dosen_filter)

    # Filterisasi Dosen
    # if dosen_filter:
    #     penelitian_list = penelitian_list.filter(dosen__NamaDosen=dosen_filter)

    selected_dosen = None
    if dosen_filter:
        penelitian_list = penelitian_list.filter(dosen__NamaDosen=dosen_filter)
        try:
            selected_dosen = Dosen.objects.get(NamaDosen=dosen_filter)
        except Dosen.DoesNotExist:
            selected_dosen = None

    paginator = Paginator(penelitian_list, 10)
    page_number = request.GET.get("page")
    penelitian = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_string = urlencode(query_params)

    selected_dosen = None
    if dosen_filter:
        try:
            selected_dosen = Dosen.objects.get(NamaDosen=dosen_filter).NamaDosen
        except Dosen.DoesNotExist:
            selected_dosen = None

    # Render template dengan data pagination
    return render(request, 'penelitian.html', {
        'penelitian': penelitian,
        'dosen_list': dosen_list,
        'search_query': search_query,
        'tahun_filter': tahun_filter,
        'tahun_start': tahun_start,
        'tahun_end': tahun_end,
        'query_string': query_string,
        'dosen_filter': dosen_filter,
        'selected_dosen': selected_dosen,
        'subject_area_list': sorted(subject_area_list),
        'selected_bidang': bidang_filter,
    })

# Function to handle the "Dosen List" view without pagination
def dosen_list(request):
    query = request.GET.get('q', '')
    dosen_list = Dosen.objects.all()

    if query:
        dosen_list = dosen_list.filter(NamaDosen__icontains=query)

    return render(request, 'dosen.html', {
        'dosen_list': dosen_list,
        'query': query,
    })

# # Download required NLTK resources
# nltk.download('stopwords')
# nltk.download('punkt')

# # Initialize RAKE for keyword extraction
# rake = Rake()

# # Function to categorize research and extract keywords
# def categorize_research():
#     research_data = PenelitianDosen.objects.filter(status='Active').values('scopus_id', 'judul', 'abstract')
#     all_keywords = []

#     for data in research_data:
#         text = data["judul"] + " " + data["abstract"]
#         rake.extract_keywords_from_text(text)
#         keywords = rake.get_ranked_phrases()
#         all_keywords.extend(keywords)
#     keyword_counts = Counter(all_keywords)

#     # Format results as a sorted list of dictionaries
#     result = sorted(
#         [{'keyword': keyword, 'count': count} for keyword, count in keyword_counts.items()],
#         key=lambda x: x['count'],
#         reverse=True
#     )
#     return result

# # API endpoint to run the categorize_research function and return results
# @require_POST
# def run_categorize_research(request):
#     hasil = categorize_research()
#     return JsonResponse({'hasil': hasil})