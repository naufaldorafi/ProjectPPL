from django.db import models

# Create your models here.
class Dosen(models.Model):
          NamaDosen = models.CharField(max_length=200, null=True)
          NIDNDosen = models.CharField(max_length=50, null=True)
          EmailAkun = models.CharField(max_length=50, null=True)
          NoTelepon = models.IntegerField(null=True)
          Keahlian = models.CharField(max_length=1)
          FotoDosen = models.ImageField(null=True, blank=True, upload_to="images/")
          
          def __str__(self):
                  return self.NamaDosen