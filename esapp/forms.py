from django import forms
from .models import Asignacion
import psycopg2
from decouple import config

def obtener_personas():
    try:
        conn = psycopg2.connect(
            dbname=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD"),
            host=config("DB_HOST"),
            port=config("DB_PORT")
        )
        cur = conn.cursor()
        cur.execute("SELECT nombre FROM personas ORDER BY nombre ASC")
        resultados = cur.fetchall()
        conn.close()
        return [(r[0], r[0]) for r in resultados]
    except:
        return []

class AsignacionForm(forms.ModelForm):
    asignado = forms.ChoiceField(choices=[], label="Asignado a")
    dependencia = forms.ChoiceField(choices=[
        ("AVALUOS", "AVALUOS"),
        ("CARTOGRAFIA", "CARTOGRAFIA"),
        ("CIUDADANIA/NOTIFICACION", "CIUDADANIA/NOTIFICACION"),
        ("JURIDICA", "JURIDICA"),
        ("MUTACIONES DE 1 y 5", "MUTACIONES DE 1 y 5"),
        ("MUTACIONES DE 2-3 y 4", "MUTACIONES DE 2-3 y 4")
    ])

    class Meta:
        model = Asignacion
        fields = ['cbmls', 'asignado', 'radicado', 'dependencia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asignado'].choices = obtener_personas()

    def clean_cbmls(self):
        cbmls = self.cleaned_data['cbmls']
        if not cbmls.isdigit() or len(cbmls) != 11:
            raise forms.ValidationError("CBMLS debe tener exactamente 11 dígitos.")
        return cbmls

    def clean_radicado(self):
        radicado = self.cleaned_data['radicado']
        if not radicado.isdigit() or len(radicado) not in [12, 13]:
            raise forms.ValidationError("Radicado debe tener 12 o 13 dígitos.")
        return radicado

    def clean(self):
        cleaned_data = super().clean()
        cbmls = cleaned_data.get('cbmls')
        radicado = cleaned_data.get('radicado')

        if cbmls and radicado:
            if Asignacion.objects.filter(cbmls=cbmls, radicado=radicado).exists():
                raise forms.ValidationError("Ya existe una asignación con ese CBMLS y radicado.")

            existente = Asignacion.objects.filter(cbmls=cbmls).first()
            if existente:
                raise forms.ValidationError(
                    f"Este CBMLS ya fue asignado anteriormente con el ID: {existente.id} y el Radicado: {existente.radicado}"
)
                



