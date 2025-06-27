from django.shortcuts import render
from .forms import AsignacionForm

def asignar(request):
    mensaje = None
    if request.method == "POST":
        form = AsignacionForm(request.POST)
        if form.is_valid():
            asignacion = form.save()
            mensaje = f"Datos guardados correctamente. ID asignado: {asignacion.id}"
            form = AsignacionForm()
    else:
        form = AsignacionForm()
    return render(request, "formulario.html", {"form": form, "mensaje": mensaje})

