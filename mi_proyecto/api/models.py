from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

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

    def clean(self):
        """Método para validar que la fecha de nacimiento no esté en el futuro"""
        if self.date_of_birth:
            # Asegurarse de que date_of_birth sea un objeto datetime.date
            if isinstance(self.date_of_birth, str):
                try:
                    self.date_of_birth = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
                except ValueError:
                    raise ValidationError("La fecha de nacimiento tiene un formato incorrecto.")
                
            if self.date_of_birth > timezone.now().date():
                raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')

    def save(self, *args, **kwargs):
        """Sobrescribir el método save para ejecutar la validación"""
        self.clean()  # Ejecuta la validación personalizada
        super().save(*args, **kwargs)