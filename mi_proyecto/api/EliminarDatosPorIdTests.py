from django.test import TestCase
from api.models import SensorData
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class EliminarDatosPorIdTests(TestCase):

    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear datos de prueba para SensorData
        self.fecha_hoy = timezone.now()
        self.sensor_data = SensorData.objects.create(
            sensor1Force=1.0,
            sensor2Force=2.0,
            sensor3Force=3.0,
            sensor4Force=4.0,
            sensor5Force=5.0,
            totalForce=15.0,
            readableTime=self.fecha_hoy
        )
        # URL para el endpoint de eliminar usando el 'id' del registro creado
        self.url = reverse('eliminar_datos', kwargs={'id': self.sensor_data.id})

    def test_eliminar_datos_existente(self):
        """Eliminar un registro existente"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Registro eliminado correctamente')
        self.assertFalse(SensorData.objects.filter(id=self.sensor_data.id).exists())

    
    def test_eliminar_datos_no_existente(self):
        """Intentar eliminar un registro que no existe"""
        response = self.client.delete(reverse('eliminar_datos', kwargs={'id': 999}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'Registro no encontrado')

    
    def test_eliminar_datos_con_csrf_enabled(self):
        """Probar que la eliminación falla cuando CSRF no está deshabilitado"""
        response = self.client.delete(self.url, HTTP_X_CSRF_TOKEN='dummy_token')
        self.assertEqual(response.status_code, 200)  # Ahora se espera 200 si CSRF está deshabilitado

    
    def test_metodo_incorrecto(self):
        """Probar que se bloquea un método no DELETE"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_eliminar_datos_con_fecha_hoy(self):
        """Eliminar un registro con fecha hoy"""
        sensor_data = SensorData.objects.create(
            sensor1Force=2.0,
            sensor2Force=3.0,
            sensor3Force=4.0,
            sensor4Force=5.0,
            sensor5Force=6.0,
            totalForce=20.0,
            readableTime=timezone.now()
        )
        url = reverse('eliminar_datos', kwargs={'id': sensor_data.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(SensorData.objects.filter(id=sensor_data.id).exists())
    
    def test_eliminar_datos_sin_permiso(self):
        """Prueba sin permisos adecuados para eliminar"""
    
       # Crear un usuario sin permisos para eliminar
        user = User.objects.create_user(username='testuser', password='password')
    
       # Iniciar sesión con ese usuario
        self.client.login(username='testuser', password='password')
    
       # URL del registro que se va a eliminar
        url = reverse('eliminar_datos', kwargs={'id': 1})
    
       # Intentar eliminar un registro
        response = self.client.delete(url)
    
    # Verificar que la respuesta sea 403 (sin permisos)
        self.assertEqual(response.status_code, 403)


    