from django.db import models
from pirogues.models import Pirogue, Position

class Alerte(models.Model):
    TYPE_CHOICES = (
        ('mayday', 'Mayday'),
        ('informations', 'Informations'),
        # Ajoutez d'autres types d'alerte si nécessaire
    )

    pirogue = models.ForeignKey(Pirogue, on_delete=models.CASCADE)
    message = models.TextField()
    type_alerte = models.CharField(max_length=20, choices=TYPE_CHOICES, default='mayday')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Récupérer la dernière position de la pirogue associée
        if self.pirogue:
            try:
                # Récupérer la dernière position de la pirogue
                last_position = Position.objects.filter(pirogue=self.pirogue).latest('timestamp')
                self.latitude = last_position.latitude
                self.longitude = last_position.longitude

            except Position.DoesNotExist:
                # Si la pirogue n'a pas de position, laisser last_pirogue_position à None
                pass

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Alerte de {self.pirogue} à {self.timestamp}"
