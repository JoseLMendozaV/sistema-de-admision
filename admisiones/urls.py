from django.urls import path

from . import views

app_name = 'admisiones'

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.registro_estudiante, name='registro_estudiante'),

    path('estudiante/', views.estudiante_dashboard, name='estudiante_dashboard'),
    path('estudiante/perfil/', views.estudiante_perfil, name='estudiante_perfil'),
    path('estudiante/entrega/<int:entrega_id>/', views.subir_enlace, name='subir_enlace'),

    path('ajax/programas/', views.programas_por_unidad, name='programas_por_unidad'),

    path('panel/', views.panel_admin, name='panel_admin'),
    path('panel/estudiante/<int:profile_id>/', views.detalle_estudiante, name='detalle_estudiante'),
    path('panel/revisar/<int:entrega_id>/', views.revisar_entrega, name='revisar_entrega'),
]