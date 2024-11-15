from django.db import models
from Dosen.models import Dosen
# Create your models here. 
class TopikPenelitian(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
    
class PenelitianDosen(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Non-Active', 'Non-Active'),
    ]
    
    author_id = models.CharField(max_length=20, null=True)
    scopus_id = models.CharField(max_length=20, unique=True, null=True)
    judul = models.CharField(max_length=1000, null=True)
    abstract = models.CharField(max_length=5000, null=True)
    tanggal_publikasi = models.DateField(null=True)
    tipe_publikasi = models.CharField(max_length=1, null=True)
    sumber = models.CharField(max_length=250, null=True)
    topik_penelitian_1 = models.ForeignKey(TopikPenelitian, on_delete=models.CASCADE, null=True, related_name='topik_penelitian_1')
    topik_penelitian_2 = models.ForeignKey(TopikPenelitian, on_delete=models.CASCADE, null=True, related_name='topik_penelitian_2')
    topik_penelitian_3 = models.ForeignKey(TopikPenelitian, on_delete=models.CASCADE, null=True, related_name='topik_penelitian_3')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    dosen = models.ForeignKey(Dosen, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.judul