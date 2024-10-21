from django.db import models

# Create your models here.   
class PenelitianDosen(models.Model):
    judul = models.CharField(max_length=100)
    abstract = models.CharField(max_length=250,null=True)
    tanggal_publikasi = models.DateField(null=True)
    tipe_publikasi = models.CharField(max_length=1,null=True)
    sumber = models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.judul
    
class TopikPenelitian(models.Model):
    nama = models.CharField(max_length=100)
    penelitiandosen_id = models.ForeignKey(PenelitianDosen, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nama