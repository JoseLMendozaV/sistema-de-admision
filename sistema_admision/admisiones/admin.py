from django.contrib import admin

from .models import Requirement, StudentProfile, StudentDocumentSubmission


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'cedula_pasaporte',
        'programa_postgrado',
        'centro_regional',
        'universidad_origen',
        'sistema_calificacion_diferente',
        'actualizado_en',
    ]
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'cedula_pasaporte',
    ]
    list_filter = [
        'universidad_origen',
        'sistema_calificacion_diferente',
        'centro_regional',
    ]


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = [
        'titulo',
        'orden',
        'aplica_a',
        'obligatorio',
        'activo',
    ]
    list_editable = [
        'orden',
        'obligatorio',
        'activo',
    ]
    search_fields = ['titulo', 'descripcion', 'codigo']
    list_filter = ['aplica_a', 'obligatorio', 'activo']


@admin.register(StudentDocumentSubmission)
class StudentDocumentSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'profile',
        'requirement',
        'estado',
        'enviado_en',
        'actualizado_en',
        'revisado_por',
    ]
    list_filter = [
        'estado',
        'requirement',
        'actualizado_en',
    ]
    search_fields = [
        'profile__user__first_name',
        'profile__user__last_name',
        'profile__user__email',
        'requirement__titulo',
        'enlace_url',
    ]