from django.db import models

class Asignacion(models.Model):
    cbmls = models.CharField(max_length=11)
    asignado = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)  # guarda la fecha actual automáticamente
    radicado = models.CharField(max_length=12)
    dependencia = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cbmls} - {self.asignado}"
