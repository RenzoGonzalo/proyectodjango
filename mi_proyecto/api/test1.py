from django.test import TestCase
from django.urls import reverse
import json
from django.contrib.auth.models import User
from api.models import UserProfile

class RegisterUserTests(TestCase):
    
    def setUp(self):
        self.url = reverse('register_user')

    def test_register_successful(self):
        """Registro exitoso con todos los campos"""
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "address": "123 Main St",
            "phone_number": "1234567890",
            "date_of_birth": "1990-01-01"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'Registro exitoso')
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_missing_email(self):
        """Registro exitoso sin campo opcional email"""
        data = {
            "username": "user_no_email",
            "password": "testpassword",
            "address": "456 Main St",
            "phone_number": "9876543210",
            "date_of_birth": "1995-05-05"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'Registro exitoso')

    def test_register_missing_username(self):
        """Falla al faltar el campo obligatorio username"""
        data = {
            "password": "testpassword",
            "email": "user_missing@example.com",
            "address": "456 Main St",
            "phone_number": "9876543210"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.json()['error'])

    def test_register_missing_password(self):
        """Falla al faltar el campo obligatorio password"""
        data = {
            "username": "user_no_password",
            "email": "user_missing@example.com",
            "address": "456 Main St",
            "phone_number": "9876543210"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.json()['error'])

    def test_register_invalid_email(self):
        """Falla por email inválido"""
        data = {
        "username": "user_invalid_email",
        "password": "testpassword",
        "email": "invalidemail",  # Correo inválido
        "address": "789 Main St",
        "phone_number": "5555555555"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
    
    # Se espera un error 400 debido a correo electrónico inválido
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email inválido', response.json()['error'])

    def test_register_duplicate_username(self):
        """Falla al intentar registrar un username duplicado"""
        User.objects.create_user(username="duplicate_user", password="password")
        data = {
            "username": "duplicate_user",
            "password": "anotherpassword",
            "email": "duplicate@example.com"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_register_invalid_phone_number(self):
        """Registro exitoso con un número de teléfono no validado (sin restricciones en el modelo)"""
        data = {
            "username": "user_invalid_phone",
            "password": "testpassword",
            "email": "valid@example.com",
            "phone_number": "notaphonenumber"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_register_date_of_birth_future(self):
        """Falla al registrar un usuario con fecha de nacimiento futura"""
        data = {
        "username": "future_user",
        "password": "testpassword",
        "email": "future@example.com",
        "date_of_birth": "2100-01-01"
        }
        response = self.client.post(self.url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)  # Ahora debería devolver un error 400
        self.assertIn('La fecha de nacimiento no puede ser en el futuro', response.json()['error'])



    def test_register_invalid_method(self):
        """Falla al intentar registrar usando un método no permitido (GET)"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error'], 'Método no permitido')

    def test_register_empty_body(self):
        """Falla al enviar una solicitud con un cuerpo vacío"""
        response = self.client.post(self.url, data={}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
