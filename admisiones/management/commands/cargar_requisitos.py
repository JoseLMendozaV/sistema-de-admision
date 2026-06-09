from django.core.management.base import BaseCommand

from admisiones.models import Requirement


class Command(BaseCommand):
    help = 'Carga los requisitos iniciales de admisión de postgrado.'

    def handle(self, *args, **options):
        requisitos = [
            {
                'orden': 1,
                'codigo': 'diploma_confrontado',
                'titulo': 'Diploma confrontado',
                'descripcion': (
                    'Dos (2) copias del diploma confrontadas contra el original '
                    'por la Secretaría General o Secretaría Académica de los Centros Regionales '
                    'de la Universidad Tecnológica de Panamá. Costo: B/. 0.50 por documento. '
                    'Si el aspirante proviene de otra universidad, debe considerar tres (3) copias '
                    'confrontadas, ya que un juego adicional se utiliza para el trámite del índice académico equivalente.'
                ),
                'aplica_a': Requirement.TODOS,
            },
            {
                'orden': 2,
                'codigo': 'creditos_universitarios',
                'titulo': 'Créditos universitarios confrontados',
                'descripcion': (
                    'Dos (2) copias de los créditos universitarios de graduado confrontadas contra '
                    'los originales por la Secretaría General o Secretaría Académica de los Centros Regionales '
                    'de la Universidad Tecnológica de Panamá. Costo: B/. 0.50 por documento. '
                    'En los créditos debe aparecer el sistema de calificación de la universidad de procedencia.'
                ),
                'aplica_a': Requirement.TODOS,
            },
            {
                'orden': 3,
                'codigo': 'fotos_carne',
                'titulo': 'Fotos tamaño carné',
                'descripcion': 'Dos (2) fotos tamaño carné.',
                'aplica_a': Requirement.TODOS,
            },
            {
                'orden': 4,
                'codigo': 'curriculum_vitae',
                'titulo': 'Curriculum Vitae',
                'descripcion': 'Curriculum Vitae actualizado del aspirante.',
                'aplica_a': Requirement.TODOS,
            },
            {
                'orden': 5,
                'codigo': 'cartas_solicitud_ingreso',
                'titulo': 'Cartas de solicitud de ingreso',
                'descripcion': (
                    'Dos (2) cartas de solicitud de ingreso, original y copia, '
                    'dirigidas al Vicedecano de Investigación, Postgrado y Extensión.'
                ),
                'aplica_a': Requirement.TODOS,
            },
            {
                'orden': 6,
                'codigo': 'cedula_pasaporte',
                'titulo': 'Cédula, pasaporte o carné de migración',
                'descripcion': (
                    'Dos (2) copias de la cédula. Los estudiantes extranjeros deben presentar '
                    'pasaporte o carné de migración vigente.'
                ),
                'aplica_a': Requirement.TODOS,
            },
            {
                'orden': 7,
                'codigo': 'indice_academico_equivalente',
                'titulo': 'Certificación de Índice Académico Equivalente',
                'descripcion': (
                    'Certificación de Índice Académico Equivalente expedida por la Secretaría General '
                    'de la Universidad Tecnológica de Panamá, para graduados de universidades con sistema '
                    'de calificación diferente al de la UTP. Costo: B/. 20.00. '
                    'Si el índice equivalente es menor al exigido, no podrá ingresar al programa.'
                ),
                'aplica_a': Requirement.SOLO_INDICE_EQUIVALENTE,
            },
            {
                'orden': 8,
                'codigo': 'formulario_admision_postgrado',
                'titulo': 'Formulario de Solicitud de Admisión de Estudios de Postgrado',
                'descripcion': (
                    'Llenar el Formulario de Solicitud de Admisión de Estudios de Postgrado. '
                    'Entregar original y una (1) copia.'
                ),
                'aplica_a': Requirement.TODOS,
            },
            {
                'orden': 9,
                'codigo': 'certificacion_ingles',
                'titulo': 'Certificación de conocimiento del idioma inglés',
                'descripcion': (
                    'Presentar certificación de conocimiento del idioma inglés. Durante el periodo '
                    'de estudio, el estudiante debe tramitar una certificación en el Centro Especializado '
                    'de Lenguas de la Universidad Tecnológica de Panamá. Esta certificación debe remitirse '
                    'a Secretaría General como requisito para graduarse.'
                ),
                'aplica_a': Requirement.TODOS,
            },
        ]

        for item in requisitos:
            Requirement.objects.update_or_create(
                codigo=item['codigo'],
                defaults=item
            )

        self.stdout.write(
            self.style.SUCCESS('Requisitos cargados correctamente.')
        )