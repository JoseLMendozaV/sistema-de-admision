from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    UTP = 'UTP'
    OTRA = 'OTRA'

    UNIVERSIDAD_CHOICES = [
        (UTP, 'Universidad Tecnológica de Panamá'),
        (OTRA, 'Otra universidad'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    cedula_pasaporte = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    programa_postgrado = models.CharField(max_length=200, blank=True)
    centro_regional = models.CharField(max_length=150, blank=True)

    universidad_origen = models.CharField(
        max_length=10,
        choices=UNIVERSIDAD_CHOICES,
        default=UTP
    )

    nombre_universidad_origen = models.CharField(max_length=200, blank=True)

    sistema_calificacion_diferente = models.BooleanField(
        default=False,
        help_text='Marcar si la universidad de origen usa un sistema de calificación distinto al de la UTP.'
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username}'

    def requiere_indice_equivalente(self):
        return self.universidad_origen == self.OTRA and self.sistema_calificacion_diferente


class Requirement(models.Model):
    TODOS = 'TODOS'
    SOLO_INDICE_EQUIVALENTE = 'INDICE_EQUIVALENTE'

    APPLIES_TO_CHOICES = [
        (TODOS, 'Todos los aspirantes'),
        (SOLO_INDICE_EQUIVALENTE, 'Solo si requiere índice académico equivalente'),
    ]

    codigo = models.SlugField(unique=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    aplica_a = models.CharField(
        max_length=30,
        choices=APPLIES_TO_CHOICES,
        default=TODOS
    )
    obligatorio = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', 'titulo']

    def __str__(self):
        return self.titulo


class StudentDocumentSubmission(models.Model):
    SIN_ENVIAR = 'SIN_ENVIAR'
    EN_REVISION = 'EN_REVISION'
    EN_PROCESO = 'EN_PROCESO'
    SUBSANAR = 'SUBSANAR'
    APROBADO = 'APROBADO'
    RECHAZADO = 'RECHAZADO'

    STATUS_CHOICES = [
        (SIN_ENVIAR, 'Sin enviar'),
        (EN_REVISION, 'En revisión'),
        (EN_PROCESO, 'En proceso'),
        (SUBSANAR, 'Subsanar'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
    ]

    profile = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='documentos'
    )

    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        related_name='entregas'
    )

    enlace_url = models.URLField(
        max_length=1000,
        blank=True,
        help_text='Enlace compartido del documento. Ejemplo: Google Drive, OneDrive, Dropbox.'
    )

    estado = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=SIN_ENVIAR
    )

    observacion_admin = models.TextField(blank=True)
    revisado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documentos_revisados'
    )

    enviado_en = models.DateTimeField(null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('profile', 'requirement')
        ordering = ['requirement__orden']

    def __str__(self):
        return f'{self.profile} - {self.requirement.titulo}'

    def badge_class(self):
        clases = {
            self.SIN_ENVIAR: 'bg-gray-100 text-gray-700 border-gray-200',
            self.EN_REVISION: 'bg-blue-100 text-blue-700 border-blue-200',
            self.EN_PROCESO: 'bg-yellow-100 text-yellow-800 border-yellow-200',
            self.SUBSANAR: 'bg-orange-100 text-orange-800 border-orange-200',
            self.APROBADO: 'bg-green-100 text-green-700 border-green-200',
            self.RECHAZADO: 'bg-red-100 text-red-700 border-red-200',
        }
        return clases.get(self.estado, 'bg-gray-100 text-gray-700 border-gray-200')