from django.urls import path
from . import views

urlpatterns = [
    path('recibir/', views.recibir_datos, name='recibir_datos'),
    path('obtener_datos/', views.obtener_datos_por_fecha, name='obtener_datos'),
    path('valores-extremos/', views.obtener_valores_extremos, name='valores_extremos'),
    path('register/', views.register_user, name='register_user'),  # Ruta para registro
    path('login/', views.login_user, name='login_user'),          # Ruta para login
    path('eliminar_datos/<int:id>/', views.eliminar_datos_por_id, name='eliminar_datos'),


]
