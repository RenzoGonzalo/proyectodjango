from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
import json


class LoginUserTests(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.login_url = reverse('login_user')

    def test_login_exitoso(self):
        """Verifica que un usuario con credenciales válidas pueda iniciar sesión."""
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Inicio de sesión exitoso")

    def test_login_credenciales_invalidas(self):
        """Verifica que un usuario con credenciales inválidas reciba un error."""
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Credenciales inválidas")

    def test_login_usuario_no_existente(self):
        """Verifica el manejo de un usuario que no existe."""
        data = {
            "username": "nonexistentuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Credenciales inválidas")

    def test_login_sin_datos(self):
        """Verifica el comportamiento cuando no se envían datos."""
        response = self.client.post(self.login_url, json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_login_metodo_no_permitido(self):
        """Verifica que un método que no sea POST retorne el error adecuado."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["error"], "Método no permitido")

    def test_login_datos_invalidos(self):
        """Verifica el comportamiento cuando se envían datos mal formateados."""
        response = self.client.post(self.login_url, "invalid-data", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_login_username_faltante(self):
        """Verifica el comportamiento cuando falta el campo 'username'."""
        data = {"password": "testpassword"}
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_login_password_faltante(self):
        """Verifica el comportamiento cuando falta el campo 'password'."""
        data = {"username": "testuser"}
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_login_datos_extra(self):
        """Verifica que datos extra en la solicitud no afecten el inicio de sesión."""
        data = {
            "username": "testuser",
            "password": "testpassword",
            "extra": "value"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Inicio de sesión exitoso")

    def test_login_datos_como_lista(self):
        """Verifica el comportamiento cuando se envía una lista en lugar de un diccionario."""
        data = ["testuser", "testpassword"]
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_login_json_malformado(self):
        """Verifica el manejo de un JSON malformado."""
        response = self.client.post(self.login_url, '{"username": "testuser", "password": "testpassword"', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_login_caso_sensible(self):
        """Verifica que el nombre de usuario sea sensible a mayúsculas/minúsculas."""
        data = {
        "username": "TestUser",  # Cambia esto para que no coincida exactamente con el nombre de usuario en la base de datos
        "password": "testpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        # Aquí deberías verificar que el código de estado sea 401 porque el nombre de usuario es sensible a mayúsculas/minúsculas
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Credenciales inválidas")


    def test_login_password_vacio(self):
        """Verifica el comportamiento cuando el campo 'password' está vacío."""
        data = {
            "username": "testuser",
            "password": ""
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Credenciales inválidas")

    def test_login_username_vacio(self):
        """Verifica el comportamiento cuando el campo 'username' está vacío."""
        data = {
            "username": "",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Credenciales inválidas")

    def test_login_usuario_inactivo(self):
        """Verifica que un usuario inactivo no pueda iniciar sesión."""
        self.user.is_active = False
        self.user.save()
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Credenciales inválidas")

    def test_login_sin_content_type(self):
        """Verifica que una solicitud sin 'Content-Type' retorne un error."""
        data = {
        "username": "testuser",
        "password": "testpassword"
        }
        # Realizar la solicitud sin Content-Type especificado
        response = self.client.post(self.login_url, data)  # No es necesario json.dumps
        self.assertEqual(response.status_code, 400)  # Espera un error 400 debido a Content-Type faltante


    def test_login_content_type_erroneo(self):
        """Verifica que una solicitud con 'Content-Type' erróneo retorne un error."""
        data = {
        "username": "testuser",
        "password": "testpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="text/plain")
        self.assertEqual(response.status_code, 400)


    def test_login_username_con_espacios(self):
        """Verifica el manejo de un nombre de usuario con espacios."""
        data = {
            "username": " testuser ",
            "password": "testpassword"
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_login_password_largo(self):
        """Verifica el manejo de un password muy largo."""
        data = {
            "username": "testuser",
            "password": "a" * 500
        }
        response = self.client.post(self.login_url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_login_solicitud_vacia(self):
        """Verifica el comportamiento cuando la solicitud está vacía."""
        response = self.client.post(self.login_url, "", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
