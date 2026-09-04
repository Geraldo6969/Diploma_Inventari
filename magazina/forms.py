from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Produkti


class RememberMeAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        label="Më mbaj mend",
        widget=forms.CheckboxInput(attrs={"class": "remember-checkbox"}),
    )


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Excel file",
        help_text="Ngarko nje file .xlsx me rreshtin e pare si emra kolonash.",
    )

    def clean_excel_file(self):
        excel_file = self.cleaned_data['excel_file']
        if not excel_file.name.lower().endswith('.xlsx'):
            raise forms.ValidationError("Ngarko vetem file Excel .xlsx.")
        return excel_file


class ProduktiForm(forms.ModelForm):
    class Meta:
        model = Produkti
        fields = [
            'emri', 
            'pershkrimi', 
            'furnitori', 
            'sasia', 
            'njesia_matese', 
            'cmimi_blerjes', 
            'cmimi_shitjes', 
            'monedha',
            'stoku_minimal',
            'data_hyrjes',
            'data_daljes',
            'data_skadences',  # SHTEZA 1: Shtohet këtu që të shfaqet në faqe
            'ne_oferte',
            'cmimi_ofertes'
        ]
        
        widgets = {
            'data_hyrjes': forms.DateInput(attrs={'type': 'date'}),
            'data_daljes': forms.DateInput(attrs={'type': 'date'}),
            'data_skadences': forms.DateInput(attrs={'type': 'date'}), # SHTEZA 2: Kthehet në kalendar
            'pershkrimi': forms.Textarea(attrs={'rows': 3}),
            'ne_oferte': forms.CheckboxInput(),
            'sasia': forms.NumberInput(attrs={'step': '0.001'}),
            'stoku_minimal': forms.NumberInput(attrs={'step': '0.001'}),
            'cmimi_blerjes': forms.NumberInput(attrs={'step': '0.001'}),
            'cmimi_shitjes': forms.NumberInput(attrs={'step': '0.001'}),
            'cmimi_ofertes': forms.NumberInput(attrs={'step': '0.001'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
            
        # SHTEZA 3: Përfshijmë edhe datën e skadencës te kontrolli i datave nëse duhet
        fushate_numrave = ['sasia', 'stoku_minimal', 'cmimi_blerjes', 'cmimi_shitjes', 'cmimi_ofertes']
        for fusha in fushate_numrave:
            if fusha in self.fields:
                if self.instance and self.instance.pk and getattr(self.instance, fusha) is not None:
                    vlera_aktuale = getattr(self.instance, fusha)
                    self.fields[fusha].initial = f"{float(vlera_aktuale):.2f}"
                    self.fields[fusha].widget.attrs['value'] = f"{float(vlera_aktuale):.2f}"
