from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Count
from datetime import date, timedelta
from .models import Asignacion
from .forms import AsignacionForm


# ✅ Función para verificar si el usuario es administrador o superusuario
def es_admin(user):
    try:
        return user.is_superuser or user.groups.filter(name__iexact='administradores').exists()
    except:
        return False


# ✅ Vista de formulario de asignación
@login_required
def asignar(request):
    mensaje = None
    advertencia = None

    if 'forzar' in request.POST:
        datos_temporales = request.session.get('datos_temporales')
        if datos_temporales:
            asignacion = Asignacion.objects.create(
                cbmls=datos_temporales['cbmls'],
                radicado=datos_temporales['radicado'],
                dependencia=datos_temporales['dependencia'],
                asignado=request.user
            )
            mensaje = f"Se creó un nuevo registro con ID: {asignacion.id} y Radicado: {asignacion.radicado}"
            request.session.pop('datos_temporales', None)
        form = AsignacionForm()
    elif request.method == 'POST':
        form = AsignacionForm(request.POST)
        if form.is_valid():
            try:
                asignacion = form.save(commit=False)
                asignacion.asignado = request.user
                asignacion.save()
                mensaje = f"Datos guardados correctamente. ES asignado: {asignacion.id}, Radicado: {asignacion.radicado}"
                form = AsignacionForm()
            except Exception:
                request.session['datos_temporales'] = form.cleaned_data
                advertencia = "Error al guardar. ¿Desea forzar el guardado?"
        else:
            mensaje = "Hay errores en el formulario."
    else:
        form = AsignacionForm()

    # ✅ Preparar datos para los gráficos (solo para usuarios normales)
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    asignaciones_usuario = Asignacion.objects.filter(asignado=request.user)

    dias = asignaciones_usuario.filter(fecha__gte=inicio_mes) \
        .values('fecha') \
        .annotate(total=Count('id')) \
        .order_by('fecha')

    barras_labels = [d['fecha'].strftime('%d/%m') for d in dias]
    barras_datos = [d['total'] for d in dias]

    dependencias = asignaciones_usuario.values('dependencia') \
        .annotate(total=Count('id')) \
        .order_by('-total')

    pie_labels = [d['dependencia'] for d in dependencias]
    pie_datos = [d['total'] for d in dependencias]

    return render(request, "formulario.html", {
        "form": form,
        "mensaje": mensaje,
        "advertencia": advertencia,
        "barras_labels": barras_labels,
        "barras_datos": barras_datos,
        "pie_labels": pie_labels,
        "pie_datos": pie_datos,
        "es_admin": es_admin(request.user),
        "debug_admin": es_admin(request.user),  # Para mensajes en template
    })


# ✅ Dashboard para administradores
@login_required
@user_passes_test(es_admin)
def dashboard(request):
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    inicio_semana = hoy - timedelta(days=hoy.weekday())

    filtro_dependencia = request.GET.get("dependencia")
    filtro_usuario = request.GET.get("usuario")

    asignaciones = Asignacion.objects.all()

    if filtro_dependencia:
        asignaciones = asignaciones.filter(dependencia=filtro_dependencia)

    if filtro_usuario:
        asignaciones = asignaciones.filter(asignado__username=filtro_usuario)

    usuarios = User.objects.filter(asignacion__in=asignaciones).distinct()

    resumen = []
    total_hoy = 0
    total_mes = 0

    for usuario in usuarios:
        hoy_count = asignaciones.filter(asignado=usuario, fecha=hoy).count()
        semana_count = asignaciones.filter(asignado=usuario, fecha__gte=inicio_semana).count()
        mes_count = asignaciones.filter(asignado=usuario, fecha__gte=inicio_mes).count()

        resumen.append({
            'usuario': usuario.get_full_name() or usuario.username,
            'usuario_username': usuario.username,
            'hoy': hoy_count,
            'semana': semana_count,
            'mes': mes_count,
        })

        total_hoy += hoy_count
        total_mes += mes_count

    resumen = sorted(resumen, key=lambda x: x['mes'], reverse=True)

    por_dependencia = (
        asignaciones
        .values('dependencia')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    labels = [item['dependencia'] for item in por_dependencia]
    datos = [item['total'] for item in por_dependencia]

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "resumen": resumen,
            "total_hoy": total_hoy,
            "total_mes": total_mes,
            "labels": labels,
            "datos": datos,
        })

    return render(request, 'dashboard.html', {
        'resumen': resumen,
        'total_hoy': total_hoy,
        'total_mes': total_mes,
        'labels': labels,
        'datos': datos,
    })


# ✅ Reporte plano para administradores
@login_required
@user_passes_test(es_admin)
def reporte(request):
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_mes = hoy.replace(day=1)

    usuarios = User.objects.filter(asignacion__isnull=False).distinct()
    resumen = []

    for usuario in usuarios:
        hoy_count = Asignacion.objects.filter(asignado=usuario, fecha=hoy).count()
        semana_count = Asignacion.objects.filter(asignado=usuario, fecha__gte=inicio_semana).count()
        mes_count = Asignacion.objects.filter(asignado=usuario, fecha__gte=inicio_mes).count()

        resumen.append({
            'usuario': usuario.get_full_name() or usuario.username,
            'hoy': hoy_count,
            'semana': semana_count,
            'mes': mes_count,
        })

    resumen = sorted(resumen, key=lambda x: x['mes'], reverse=True)

    return render(request, 'reporte.html', {
        'resumen': resumen
    })
