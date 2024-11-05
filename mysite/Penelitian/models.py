from django.db import models

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
    
    scopus_id = models.CharField(max_length=20, unique=True, null=True)  # Scopus ID placed before Judul
    judul = models.CharField(max_length=100)
    abstract = models.CharField(max_length=250, null=True)
    tanggal_publikasi = models.DateField(null=True)
    tipe_publikasi = models.CharField(max_length=1, null=True)
    sumber = models.CharField(max_length=250, null=True)
    topikpenelitian_id = models.ForeignKey(TopikPenelitian, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    def __str__(self):
        return self.judul