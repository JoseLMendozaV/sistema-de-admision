from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from .models import Requirement, StudentProfile, StudentDocumentSubmission, AcademicUnit, GraduateProgram

from .forms import (
    RegistroEstudianteForm,
    StudentProfileForm,
    StudentDocumentSubmissionForm,
    AdminReviewForm,
)
from .models import Requirement, StudentProfile, StudentDocumentSubmission


def es_admin(user):
    return user.is_authenticated and user.is_staff


def home(request):
    return render(request, 'admisiones/home.html')


def registro_estudiante(request):
    if request.method == 'POST':
        form = RegistroEstudianteForm(request.POST)

        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente. Complete su perfil de admisión.')
            return redirect('admisiones:estudiante_perfil')
    else:
        form = RegistroEstudianteForm()

    return render(request, 'admisiones/registro.html', {'form': form})


def obtener_perfil_estudiante(user):
    profile, _ = StudentProfile.objects.get_or_create(user=user)
    return profile


def requisitos_aplicables(profile):
    requisitos = Requirement.objects.filter(activo=True)

    if not profile.requiere_indice_equivalente():
        requisitos = requisitos.exclude(aplica_a=Requirement.SOLO_INDICE_EQUIVALENTE)

    return requisitos.order_by('orden')


def sincronizar_entregas(profile):
    requisitos = requisitos_aplicables(profile)

    for requisito in requisitos:
        StudentDocumentSubmission.objects.get_or_create(
            profile=profile,
            requirement=requisito
        )

    return StudentDocumentSubmission.objects.filter(
        profile=profile,
        requirement__in=requisitos
    ).select_related('requirement')


@login_required
def estudiante_dashboard(request):
    if request.user.is_staff:
        return redirect('admisiones:panel_admin')

    profile = obtener_perfil_estudiante(request.user)
    entregas = sincronizar_entregas(profile)

    total = entregas.count()
    aprobados = entregas.filter(estado=StudentDocumentSubmission.APROBADO).count()
    enviados = entregas.exclude(estado=StudentDocumentSubmission.SIN_ENVIAR).count()

    porcentaje_aprobado = int((aprobados / total) * 100) if total else 0
    porcentaje_enviado = int((enviados / total) * 100) if total else 0

    contexto = {
        'profile': profile,
        'entregas': entregas,
        'total': total,
        'aprobados': aprobados,
        'enviados': enviados,
        'porcentaje_aprobado': porcentaje_aprobado,
        'porcentaje_enviado': porcentaje_enviado,
    }

    return render(request, 'admisiones/estudiante_dashboard.html', contexto)


@login_required
def estudiante_perfil(request):
    if request.user.is_staff:
        return redirect('admisiones:panel_admin')

    profile = obtener_perfil_estudiante(request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('admisiones:estudiante_dashboard')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'admisiones/estudiante_perfil.html', {
        'form': form,
        'profile': profile,
    })


@login_required
def subir_enlace(request, entrega_id):
    if request.user.is_staff:
        return redirect('admisiones:panel_admin')

    profile = obtener_perfil_estudiante(request.user)

    entrega = get_object_or_404(
        StudentDocumentSubmission,
        id=entrega_id,
        profile=profile
    )

    if request.method == 'POST':
        form = StudentDocumentSubmissionForm(request.POST, instance=entrega)

        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.estado = StudentDocumentSubmission.EN_REVISION
            entrega.enviado_en = timezone.now()
            entrega.revisado_por = None
            entrega.save()

            messages.success(
                request,
                'Enlace enviado correctamente. El documento queda en revisión.'
            )
            return redirect('admisiones:estudiante_dashboard')
    else:
        form = StudentDocumentSubmissionForm(instance=entrega)

    return render(request, 'admisiones/subir_enlace.html', {
        'form': form,
        'entrega': entrega,
    })


@user_passes_test(es_admin)
def panel_admin(request):
    perfiles = StudentProfile.objects.select_related('user').annotate(
        total_documentos=Count('documentos'),
        aprobados=Count(
            'documentos',
            filter=Q(documentos__estado=StudentDocumentSubmission.APROBADO)
        ),
        en_revision=Count(
            'documentos',
            filter=Q(documentos__estado=StudentDocumentSubmission.EN_REVISION)
        ),
        subsanar=Count(
            'documentos',
            filter=Q(documentos__estado=StudentDocumentSubmission.SUBSANAR)
        ),
    ).order_by('-actualizado_en')

    return render(request, 'admisiones/panel_admin.html', {
        'perfiles': perfiles,
    })


@user_passes_test(es_admin)
def detalle_estudiante(request, profile_id):
    profile = get_object_or_404(
        StudentProfile.objects.select_related('user'),
        id=profile_id
    )

    sincronizar_entregas(profile)

    entregas = StudentDocumentSubmission.objects.filter(
        profile=profile
    ).select_related('requirement')

    return render(request, 'admisiones/detalle_estudiante.html', {
        'profile': profile,
        'entregas': entregas,
    })


@user_passes_test(es_admin)
def revisar_entrega(request, entrega_id):
    entrega = get_object_or_404(
        StudentDocumentSubmission.objects.select_related('profile', 'requirement'),
        id=entrega_id
    )

    if request.method == 'POST':
        form = AdminReviewForm(request.POST, instance=entrega)

        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.revisado_por = request.user
            entrega.save()

            messages.success(request, 'Estado actualizado correctamente.')
            return redirect('admisiones:detalle_estudiante', profile_id=entrega.profile.id)

    return redirect('admisiones:detalle_estudiante', profile_id=entrega.profile.id)


@login_required
def programas_por_unidad(request):
    unidad_id = request.GET.get('unidad_id')

    programas = GraduateProgram.objects.filter(
        unidad_academica_id=unidad_id,
        activo=True
    ).order_by('orden', 'nombre')

    data = [
        {
            'id': programa.id,
            'nombre': programa.nombre,
        }
        for programa in programas
    ]

    return JsonResponse({'programas': data})