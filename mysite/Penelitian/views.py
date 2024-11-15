from django.shortcuts import render
from django.core.paginator import Paginator
from .models import PenelitianDosen
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import nltk
from rake_nltk import Rake
from collections import Counter

def Penelitian(request):
    penelitian_list = PenelitianDosen.objects.all()
    paginator = Paginator(penelitian_list, 10)  # Menampilkan 10 penelitian per halaman.

    page_number = request.GET.get("page")
    penelitian = paginator.get_page(page_number)

    return render(request, 'penelitian.html', {'penelitian': penelitian})

# Unduh sumber daya yang diperlukan
nltk.download('stopwords')
nltk.download('punkt')

# Inisialisasi RAKE
rake = Rake()

# Fungsi untuk ekstraksi kata kunci dan menghitung kemunculan
def categorize_research():
    research_data = PenelitianDosen.objects.filter(status='Active', author_id='57210671389').values('scopus_id', 'judul', 'abstract')
    all_keywords = []  # Untuk menyimpan semua keyword dari seluruh penelitian

    for data in research_data:
        text = data["judul"] + " " + data["abstract"]

        # Ekstraksi kata kunci menggunakan RAKE
        rake.extract_keywords_from_text(text)
        keywords = rake.get_ranked_phrases()

        # Gabungkan semua keyword ke dalam list all_keywords
        all_keywords.extend(keywords)

    # Hitung kemunculan setiap keyword
    keyword_counts = Counter(all_keywords)

    # Format dan urutkan hasil berdasarkan count dari tertinggi ke terendah
    result = sorted(
        [{'keyword': keyword, 'count': count} for keyword, count in keyword_counts.items()],
        key=lambda x: x['count'],
        reverse=True
    )
    return result

@require_POST
def run_categorize_research(request):
    hasil = categorize_research()
    return JsonResponse({'hasil': hasil})