from django.db import models

# Create your models here.
class Histori(models.Model):
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tanggal

class KataKunci(models.Model):
    nama = models.CharField(max_length=100)
    jenis = models.CharField(max_length=1)
    kategori = models.CharField(max_length=1)

    def __str__(self):
        return self.nama