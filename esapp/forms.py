from django import forms
from .models import Asignacion, DummyRadicado  # DummyRadicado apunta a zcatt_sgto_trmte


class AsignacionForm(forms.ModelForm):
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
        fields = ['cbmls', 'radicado', 'dependencia']

    def clean_cbmls(self):
        cbmls = self.cleaned_data.get('cbmls')
        if not cbmls or not cbmls.isdigit() or len(cbmls) != 11:
            raise forms.ValidationError("El CBMLS debe tener exactamente 11 dígitos numéricos.")
        return cbmls

    def clean_radicado(self):
        radicado = self.cleaned_data.get('radicado')

        # Validación de formato
        if not radicado or not radicado.isdigit() or len(radicado) not in [12, 13]:
            raise forms.ValidationError("El Radicado debe tener 12 o 13 dígitos numéricos.")

        # Validación contra la tabla en la base de datos secundaria
        if not DummyRadicado.objects.using('secundaria').filter(nm_solicitud=radicado).exists():
            raise forms.ValidationError("El número de radicado no existe en la base de datos oficial.")

        return radicado

    def clean(self):
        cleaned_data = super().clean()
        cbmls = cleaned_data.get('cbmls')
        radicado = cleaned_data.get('radicado')

        # Puedes agregar validaciones cruzadas aquí si lo deseas
        # Ejemplo:
        # if cbmls and radicado and cbmls[-3:] == radicado[-3:]:
        #     raise forms.ValidationError("El CBMLS y Radicado no deben terminar igual.")
        
        return cleaned_data