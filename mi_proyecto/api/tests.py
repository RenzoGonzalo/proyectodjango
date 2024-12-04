import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from .models import SensorData
from django.urls import reverse

from django.utils.timezone import make_aware

class SensorDataTests(TestCase):

    

    def test_recibir_datos_correctos(self):
        url = reverse('recibir_datos')
        data = {
            "sensor1Force": 10.5,
            "sensor2Force": 20.2,
            "sensor3Force": 30.3,
            "sensor4Force": 40.4,
            "sensor5Force": 50.5,
            "totalForce": 151.9,
            "readableTime": "2024-12-03T15:30:00"
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Datos enviados correctamente')

    def test_recibir_datos_faltante_sensor(self):
        url = reverse('recibir_datos')
        data = {
            "sensor1Force": 10.5,
            "sensor2Force": 20.2,
            "sensor3Force": 30.3,
            "sensor4Force": 40.4,
            "totalForce": 151.9,
            "readableTime": "2024-12-03T15:30:00"
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    

    def test_recibir_datos_fecha_invalida(self):
        # Asegúrate de que 'recibir_datos' esté correctamente mapeada en tu archivo urls.py
        url = reverse('recibir_datos')
        
        # Los datos con fecha inválida
        data = {
            "sensor1Force": 10.5,
            "sensor2Force": 20.2,
            "sensor3Force": 30.3,
            "sensor4Force": 40.4,
            "sensor5Force": 50.5,
            "totalForce": 151.9,
            "readableTime": "invalid-date"  # Fecha incorrecta
        }
        
        # Realiza la solicitud POST
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        
        # Verifica que el código de estado sea 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        
        # Verifica que el mensaje de error esté presente en la respuesta JSON
        self.assertIn('error', response.json())

    def test_obtener_datos_por_fecha_correctos(self):
    # Crear una fecha válida en formato 'YYYY-MM-DD'
        fecha = timezone.now().date()  # Solo la parte de fecha, no datetime completo
    
    # Crear un objeto SensorData con la fecha actual
        SensorData.objects.create(
            sensor1Force=10.5, sensor2Force=20.2, sensor3Force=30.3,
            sensor4Force=40.4, sensor5Force=50.5, totalForce=151.9,
            readableTime=timezone.now()  # Asegurar que coincide con la fecha
        )
    
    # Construir la URL con el formato correcto de fecha
        url = reverse('obtener_datos') + f'?fecha={fecha}'
    
    # Hacer la solicitud GET
        response = self.client.get(url)
    
    # Verificar que la respuesta tiene estado 200
        self.assertEqual(response.status_code, 200)
    
    # Verificar que la respuesta contiene datos
        datos = response.json()
        self.assertTrue(len(datos) > 0)
    
    # Verificar que los datos retornados tienen las claves esperadas
        esperado = {'sensor1Force', 'sensor2Force', 'sensor3Force', 'sensor4Force', 'sensor5Force', 'totalForce', 'readableTime'}
        self.assertTrue(all(esperado.issubset(d.keys()) for d in datos))


    def test_obtener_datos_por_fecha_no_encontrados(self):
        # Construir la URL correctamente
        url = reverse('obtener_datos') + '?fecha=2023-12-01'
        
        # Realizar la solicitud GET
        response = self.client.get(url)
        
        # Verificar que el estado sea 404
        self.assertEqual(response.status_code, 404)
        
        # Verificar que el mensaje sea el esperado
        self.assertEqual(response.json()['message'], 'No hay datos para la fecha proporcionada')


    def test_obtener_datos_por_fecha_fecha_invalida(self):
    # Usar el nombre correcto de la vista 'obtener_datos'
        url = reverse('obtener_datos') + '?fecha=2024-02-30'
    
    # Hacer una solicitud GET con una fecha inválida
        response = self.client.get(url)
    
    # Verificar que la respuesta tenga un código de estado 400
        self.assertEqual(response.status_code, 400)
    
    # Verificar que el mensaje sea el esperado
        self.assertEqual(response.json()['error'], 'Fecha inválida')


    def test_obtener_datos_por_fecha_sin_fecha(self):
    # Usar el nombre correcto de la vista
        url = reverse('obtener_datos')  # Cambiado de 'obtener_datos_por_fecha' a 'obtener_datos'
    
    # Realizar una solicitud GET al endpoint sin enviar la fecha
        response = self.client.get(url)
    
    # Verificar que el código de estado HTTP es 400
        self.assertEqual(response.status_code, 400)
    
    # Verificar que el mensaje de error es el esperado
        self.assertEqual(response.json()['error'], 'Fecha no proporcionada')


    # Funcion 2 Register
    