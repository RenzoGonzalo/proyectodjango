from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.db.models import Max, Min
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods  # Import added here
from .models import SensorData, UserProfile
import json
from .models import SensorData
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.utils import timezone


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
            email = data.get('email', '')
            address = data.get('address', '')
            phone_number = data.get('phone_number', '')
            date_of_birth = data.get('date_of_birth', None)

            # Crear usuario
            user = User.objects.create_user(username=username, password=password, email=email)

            # Crear perfil asociado
            UserProfile.objects.create(
                user=user,
                address=address,
                phone_number=phone_number,
                date_of_birth=date_of_birth
            )

            return JsonResponse({'message': 'Registro exitoso'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({'message': 'Inicio de sesión exitoso'}, status=200)
            else:
                return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def recibir_datos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor1Force = data['sensor1Force']
            sensor2Force = data['sensor2Force']
            sensor3Force = data['sensor3Force']
            sensor4Force = data['sensor4Force']
            sensor5Force = data['sensor5Force']
            totalForce = data['totalForce']
            readableTime = parse_datetime(data['readableTime'])

            sensor_data = SensorData(
                sensor1Force=sensor1Force,
                sensor2Force=sensor2Force,
                sensor3Force=sensor3Force,
                sensor4Force=sensor4Force,
                sensor5Force=sensor5Force,
                totalForce=totalForce,
                readableTime=readableTime
            )
            sensor_data.save()

            return JsonResponse({'message': 'Datos enviados correctamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_datos_por_fecha(request):
    fecha_str = request.GET.get('fecha')  # fecha en formato 'YYYY-MM-DD'
    if fecha_str:
        fecha = parse_datetime(fecha_str)  # Convierte la fecha a datetime
        if fecha:
            # Convertir la fecha naive a fecha con zona horaria (si es necesario)
            fecha = timezone.make_aware(fecha, timezone.get_current_timezone())

            # Definir el rango de la fecha: desde las 00:00:00 hasta las 23:59:59
            inicio_fecha = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
            fin_fecha = fecha.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Filtrar los datos que están dentro de ese rango de fecha
            sensor_data = SensorData.objects.filter(readableTime__range=(inicio_fecha, fin_fecha))

            if not sensor_data.exists():
                return JsonResponse({'message': 'No hay datos para la fecha proporcionada'}, status=404)

            return JsonResponse(list(sensor_data.values()), safe=False)

        else:
            return JsonResponse({'error': 'Fecha inválida'}, status=400)
    return JsonResponse({'error': 'Fecha no proporcionada'}, status=400)

def obtener_valores_extremos(request):
    fecha_str = request.GET.get('fecha')
    if not fecha_str:
        return JsonResponse({'error': 'Debe proporcionar una fecha en formato YYYY-MM-DD'}, status=400)

    try:
        fecha_inicio = parse_datetime(fecha_str)
        fecha_fin = fecha_inicio.replace(hour=23, minute=59, second=59)

        valores = SensorData.objects.filter(readableTime__range=(fecha_inicio, fecha_fin)).aggregate(
            max_total=Max('totalForce'),
            min_total=Min('totalForce')
        )

        return JsonResponse({
            'fecha': fecha_str,
            'max_total': valores['max_total'],
            'min_total': valores['min_total']
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': f'Ocurrió un error: {str(e)}'}, status=500)

@csrf_exempt  # Deshabilitar CSRF si es necesario
@require_http_methods(["DELETE"])  # Asegura que solo se acepte DELETE
def eliminar_datos_por_id(request, id):  # Ahora capturamos 'id' desde la URL
    try:
        # Buscar el registro en la base de datos usando el 'id' desde la URL
        registro = SensorData.objects.get(id=id)
        # Eliminar el registro
        registro.delete()
        return JsonResponse({'message': 'Registro eliminado correctamente'}, status=200)
    except SensorData.DoesNotExist:
        return JsonResponse({'error': 'Registro no encontrado'}, status=404)
