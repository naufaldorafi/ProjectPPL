from django.db import models

# Create your models here.
class Dosen(models.Model):
          NamaDosen = models.CharField(max_length=50)
          EmailAkun = models.CharField(max_length=30)
          NoTelepon = models.IntegerField(null=True)
          Keahlian = models.CharField(max_length=1)
          
          def str(self):
                  return self.NamaDosen