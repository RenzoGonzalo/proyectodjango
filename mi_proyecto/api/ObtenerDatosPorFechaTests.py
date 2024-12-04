from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, make_aware, timedelta
from api.models import SensorData
import json

class ObtenerDatosPorFechaTests(TestCase):

    def setUp(self):
        # Crear datos de ejemplo
        self.fecha_actual = now()
        self.fecha_hoy = self.fecha_actual.replace(hour=10, minute=0, second=0, microsecond=0)
        self.fecha_ayer = self.fecha_actual - timedelta(days=1)
        self.fecha_mañana = self.fecha_actual + timedelta(days=1)

        # Datos para la fecha de hoy
        SensorData.objects.create(sensor1Force=1.1, sensor2Force=2.2, sensor3Force=3.3,
        sensor4Force=4.4, sensor5Force=5.5, totalForce=16.5,
        readableTime=self.fecha_hoy)

        # Datos para ayer
        SensorData.objects.create(sensor1Force=2.1, sensor2Force=3.2, sensor3Force=4.3,
        sensor4Force=5.4, sensor5Force=6.5, totalForce=21.5,
        readableTime=self.fecha_ayer)

        # Endpoint a probar
        self.url = reverse('obtener_datos')

    def test_datos_fecha_hoy(self):
        """Datos disponibles para la fecha de hoy"""
        response = self.client.get(self.url, {'fecha': self.fecha_hoy.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_datos_fecha_ayer(self):
        """Datos disponibles para la fecha de ayer"""
        response = self.client.get(self.url, {'fecha': self.fecha_ayer.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_datos_fecha_sin_datos(self):
        """Fecha válida pero sin datos disponibles"""
        fecha_sin_datos = self.fecha_actual - timedelta(days=10)
        response = self.client.get(self.url, {'fecha': fecha_sin_datos.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 404)

    def test_datos_sin_parametro_fecha(self):
        """Solicitud sin parámetro de fecha"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_datos_fecha_invalida(self):
        """Formato de fecha inválido"""
        response = self.client.get(self.url, {'fecha': 'fecha_invalida'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_datos_formato_fecha_americano(self):
        """Formato de fecha incorrecto (MM-DD-YYYY)"""
        fecha_incorrecta = self.fecha_actual.strftime('%m-%d-%Y')
        response = self.client.get(self.url, {'fecha': fecha_incorrecta})
        self.assertEqual(response.status_code, 400)

    def test_datos_rango_incorrecto(self):
        """Fecha fuera del rango permitido"""
        fecha_fuera_rango = now() + timedelta(days=1000)
        response = self.client.get(self.url, {'fecha': fecha_fuera_rango.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 404)

    def test_datos_multiple_por_fecha(self):
        """Múltiples datos en la misma fecha"""
        SensorData.objects.create(sensor1Force=1.2, sensor2Force=2.3, sensor3Force=3.4,
        sensor4Force=4.5, sensor5Force=5.6, totalForce=17.0,
        readableTime=self.fecha_hoy)
        response = self.client.get(self.url, {'fecha': self.fecha_hoy.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

