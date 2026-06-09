from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import StudentProfile, StudentDocumentSubmission


INPUT_CLASS = (
    'w-full rounded-xl border border-gray-300 px-4 py-3 '
    'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
)

CHECKBOX_CLASS = 'h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500'


class RegistroEstudianteForm(UserCreationForm):
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': INPUT_CLASS})
    )
    last_name = forms.CharField(
        label='Apellido',
        widget=forms.TextInput(attrs={'class': INPUT_CLASS})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': INPUT_CLASS})
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

        for field in self.fields.values():
            field.widget.attrs.update({'class': INPUT_CLASS})


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'cedula_pasaporte',
            'telefono',
            'programa_postgrado',
            'centro_regional',
            'universidad_origen',
            'nombre_universidad_origen',
            'sistema_calificacion_diferente',
        ]

        labels = {
            'cedula_pasaporte': 'Cédula, pasaporte o carné de migración',
            'telefono': 'Teléfono',
            'programa_postgrado': 'Programa de postgrado al que aplica',
            'centro_regional': 'Facultad o Centro Regional',
            'universidad_origen': 'Universidad de origen',
            'nombre_universidad_origen': 'Nombre de la universidad de origen',
            'sistema_calificacion_diferente': '¿El sistema de calificación es diferente al de la UTP?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': CHECKBOX_CLASS})
            else:
                field.widget.attrs.update({'class': INPUT_CLASS})


class StudentDocumentSubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentDocumentSubmission
        fields = ['enlace_url']

        labels = {
            'enlace_url': 'Enlace URL del documento compartido'
        }

        widgets = {
            'enlace_url': forms.URLInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'https://drive.google.com/...',
            })
        }


class AdminReviewForm(forms.ModelForm):
    class Meta:
        model = StudentDocumentSubmission
        fields = ['estado', 'observacion_admin']

        labels = {
            'estado': 'Estado',
            'observacion_admin': 'Observación para el estudiante',
        }

        widgets = {
            'estado': forms.Select(attrs={'class': INPUT_CLASS}),
            'observacion_admin': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                'rows': 4,
                'placeholder': 'Escriba observaciones, correcciones o indicaciones para el estudiante.'
            })
        }