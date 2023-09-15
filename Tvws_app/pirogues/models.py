from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Pirogue(AbstractUser):
    tel = models.CharField(max_length=15)
    is_marine = models.BooleanField(default=False)

    def __str__(self):
            return f"{self.first_name} {self.last_name}"
    

class Position(models.Model):
    pirogue= models.ForeignKey(Pirogue, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Position de {self.first_name} {self.last_name} à {self.timestamp}"