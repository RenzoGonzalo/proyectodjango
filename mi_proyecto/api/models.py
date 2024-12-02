from django.db import models
from django.contrib.auth.models import User

class SensorData(models.Model):
    sensor1Force = models.FloatField()  # Sensor 1
    sensor2Force = models.FloatField()  # Sensor 2
    sensor3Force = models.FloatField()  # Sensor 3
    sensor4Force = models.FloatField()  # Sensor 4
    sensor5Force = models.FloatField()  # Sensor 5
    totalForce = models.FloatField()    # Fuerza total
    readableTime = models.DateTimeField()  # Hora legible

    def __str__(self):
        return f"Datos de sensores - {self.readableTime}"

    class Meta:
        verbose_name = "Sensor Data"
        verbose_name_plural = "Sensor Data"

# Modelo extendido para usuarios
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"
    