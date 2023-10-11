from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from geopy.distance import geodesic

class Pirogue(AbstractUser):
    tel = models.CharField(max_length=15,blank=True,null=True)
    is_marine = models.BooleanField(default=False)

    def __str__(self):
            return f"{self.first_name} {self.last_name}"
    

class Position(models.Model):
    pirogue= models.ForeignKey(Pirogue, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    temps_transmission = models.FloatField(null=True, blank=True)  # Temps en secondes
    vitesse = models.FloatField(null=True, blank=True)  # Vitesse en m/s
    is_visible = models.BooleanField(default=True)  # Nouveau champ is_visible
    SECURITE_CHOICES = (
        ('vert', 'Vert'),
        ('orange', 'Orange'),
        ('rouge', 'Rouge'),
    )
    securite = models.CharField(max_length=10, choices=SECURITE_CHOICES)  # Nouveau champ securite
    def calculate_security_level(self):
        """
        Calcule et retourne le niveau de sécurité en fonction des critères.
        """
        current_time = timezone.now()
        fifteen_minutes_ago = current_time - timezone.timedelta(minutes=15)
        
        nearby_positions = Position.objects.filter(
            timestamp__gte=fifteen_minutes_ago,
            
        ).exclude(pk=self.pk)
        
        user_position = (self.latitude, self.longitude)
        security_level = 'orange'  # Valeur par défaut
        
        for position in nearby_positions:
            distance = geodesic(user_position, (position.latitude, position.longitude)).kilometers
            if distance <= 20:
                security_level = 'vert'
                break  # On a trouvé au moins une pirogue à moins de 20 km, on passe en orange
        
        return security_level
    
    def calculate_temps_transmission(self):
        """
        Calcule et met à jour le temps de transmission en fonction de la vitesse de l'utilisateur.
        """
        # On suppose que la distance est de 200 mètres
        distance_meters = 200
        
        if self.vitesse:
            self.temps_transmission = distance_meters / int(self.vitesse)
        else:
            self.temps_transmission = None

    def save(self, *args, **kwargs):
        self.calculate_temps_transmission()
        # super().save(*args, **kwargs)
        self.securite = self.calculate_security_level()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Position de {self.pirogue.first_name} {self.pirogue.last_name} à {self.timestamp}"
    
    
class NetworkInfo(models.Model):
    position = models.OneToOneField(Position, on_delete=models.CASCADE)
    operator_name = models.CharField(max_length=100)  # Nom de l'opérateur
    signal_strength = models.IntegerField()  # Puissance du signal
    network_type = models.CharField(max_length=20)  # Type de réseau (Wi-Fi, 2G, 3G, 4G, LTE, etc.)
    wifi_ssid = models.CharField(max_length=100, null=True, blank=True)  # SSID du réseau Wi-Fi
    wifi_link_speed = models.IntegerField(null=True, blank=True)  # Débit du Wi-Fi

    def __str__(self):
        return f"Network Info for Position at {self.position.timestamp}"