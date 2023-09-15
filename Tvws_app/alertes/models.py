from django.db import models
from pirogues.models import Pirogue

class Alerte(models.Model):
    TYPE_CHOICES = (
        ('mayday', 'Mayday'),
        ('informations', 'Informations'),
        # Ajoutez d'autres types d'alerte si nécessaire
    )

    pirogue = models.ForeignKey(Pirogue, on_delete=models.CASCADE)
    message = models.TextField()
    type_alerte = models.CharField(max_length=20, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerte de {self.pirogue} à {self.timestamp}"
