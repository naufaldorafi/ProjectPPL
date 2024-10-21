from django.db import models

# Create your models here.
class Akun(models.Model):
    Username = models.CharField(max_length=25)
    Password = models.CharField(max_length=25)
    Email = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.Username}, {self.Password}, {self.Email}"

    