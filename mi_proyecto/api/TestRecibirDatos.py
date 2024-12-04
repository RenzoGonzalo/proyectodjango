from django.test import TestCase
from django.urls import reverse
import json

class TestRecibirDatos(TestCase):
    def test_recibir_datos_exitoso(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': 10.0,
            'sensor2Force': 20.0,
            'sensor3Force': 30.0,
            'sensor4Force': 40.0,
            'sensor5Force': 50.0,
            'totalForce': 150.0,
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Datos enviados correctamente'})
    def test_recibir_datos_datos_incompletos(self):
        url = reverse('recibir_datos')
        data = {
            'sensor2Force': 20.0,
            'sensor3Force': 30.0,
            'sensor4Force': 40.0,
            'sensor5Force': 50.0,
            'totalForce': 150.0,
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_recibir_datos_fecha_invalida(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': 10.0,
            'sensor2Force': 20.0,
            'sensor3Force': 30.0,
            'sensor4Force': 40.0,
            'sensor5Force': 50.0,
            'totalForce': 150.0,
            'readableTime': 'invalid_date'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_recibir_datos_metodo_no_permitido(self):
        url = reverse('recibir_datos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'Método no permitido'})
    def test_recibir_datos_valores_negativos(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': -10.0,
            'sensor2Force': -20.0,
            'sensor3Force': -30.0,
            'sensor4Force': -40.0,
            'sensor5Force': -50.0,
            'totalForce': -150.0,
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Datos enviados correctamente'})
    def test_recibir_datos_valores_decimales(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': 10.5,
            'sensor2Force': 20.5,
            'sensor3Force': 30.5,
            'sensor4Force': 40.5,
            'sensor5Force': 50.5,
            'totalForce': 152.5,
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Datos enviados correctamente'})
    def test_recibir_datos_valores_nulos(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': None,
            'sensor2Force': None,
            'sensor3Force': None,
            'sensor4Force': None,
            'sensor5Force': None,
            'totalForce': None,
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    def test_recibir_datos_tipo_incorrecto(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': 'string',
            'sensor2Force': 'string',
            'sensor3Force': 'string',
            'sensor4Force': 'string',
            'sensor5Force': 'string',
            'totalForce': 'string',
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    def test_recibir_datos_datos_vacios(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': 0.0,
            'sensor2Force': 0.0,
            'sensor3Force': 0.0,
            'sensor4Force': 0.0,
            'sensor5Force': 0.0,
            'totalForce': 0.0,
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Datos enviados correctamente'})
    def test_recibir_datos_totalForce_incorrecto(self):
        url = reverse('recibir_datos')
        data = {
            'sensor1Force': 10.0,
            'sensor2Force': 20.0,
            'sensor3Force': 30.0,
            'sensor4Force': 40.0,
            'sensor5Force': 50.0,
            'totalForce': 500.0,  # Exceso de valor
            'readableTime': '2024-12-04T12:00:00'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Datos enviados correctamente'})

    
  # Prueas de registro
    def test_register_user_exitoso(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'password': 'password123',
            'email': 'user@example.com',
            'address': '123 Main St',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Registro exitoso'})
    def test_register_user_email_invalido(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'password': 'password123',
            'email': 'invalidemail',
            'address': '123 Main St',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'Email inválido'})
    def test_register_user_sin_email(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'password': 'password123',
            'address': '123 Main St',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Registro exitoso'})

        
    def test_register_user_fecha_nacimiento_futura(self):
        url = reverse('register_user')
        data = {
        'username': 'newuser',
        'password': 'password123',
        'email': 'user@example.com',
        'address': '123 Main St',
        'phone_number': '1234567890',
        'date_of_birth': '3000-01-01'  # Fecha futura
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'La fecha de nacimiento no puede ser en el futuro.'})

    def test_register_user_telefono_vacio(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'password': 'password123',
            'email': 'user@example.com',
            'address': '123 Main St',
            'phone_number': '',  # Teléfono vacío
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Registro exitoso'})

    def test_register_user_metodo_incorrecto(self):
        url = reverse('register_user')
        response = self.client.get(url)  # Usando GET en lugar de POST
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'Método no permitido'})

    def test_register_user_sin_direccion(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'password': 'password123',
            'email': 'user@example.com',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'message': 'Registro exitoso'})
    def test_register_user_sin_contraseña(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'email': 'user@example.com',
            'address': '123 Main St',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'La contraseña es obligatoria'})
    def test_register_user_sin_contraseña(self):
        url = reverse('register_user')
        data = {
            'username': 'newuser',
            'email': 'user@example.com',
            'address': '123 Main St',
            'phone_number': '1234567890',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'error': 'La contraseña es obligatoria'})