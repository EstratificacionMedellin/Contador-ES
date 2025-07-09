from django.db import models
from django.contrib.auth.models import User

class Asignacion(models.Model):
    cbmls = models.CharField(max_length=50)
    radicado = models.CharField(max_length=50)
    dependencia = models.CharField(max_length=100)
    asignado = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.radicado} - {self.cbmls}"

class DummyRadicado(models.Model):
    nm_solicitud = models.CharField(max_length=100, db_column='nm_solicitud')

    class Meta:
        managed = False  # Django no intentará crear o modificar esta tabla
        db_table = 'zcatt_sgto_trmte'
         


