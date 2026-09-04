from io import BytesIO

import os
import qrcode
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models
from django.utils.text import get_valid_filename


def validate_max_50_words(value):
    if value and len(value.split()) > 50:
        raise ValidationError("Pershkrimi nuk mund te kete me shume se 50 fjale.")


def has_decimal_part(value):
    return value is not None and value != value.to_integral_value()


class Produkti(models.Model):
    NJESIA_CHOICES = [
        ('KG', 'Kilogram'),
        ('L', 'Litër'),
        ('COPE', 'Copë'),
        ('KUTI', 'Kuti'),
    ]

    MONEDHA_CHOICES = [
        ('ALL', 'Lek'),
        ('EUR', 'Euro'),
        ('USD', 'Dollar'),
    ]

    emri = models.CharField(max_length=200)
    pershkrimi = models.TextField(blank=True, default='', validators=[validate_max_50_words])
    furnitori = models.CharField(max_length=200, blank=True, null=True)
    sasia = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    njesia_matese = models.CharField(max_length=10, choices=NJESIA_CHOICES, default='COPE')

    monedha = models.CharField(max_length=3, choices=MONEDHA_CHOICES, default='ALL')
    cmimi_blerjes = models.DecimalField(max_digits=10, decimal_places=3)
    cmimi_shitjes = models.DecimalField(max_digits=10, decimal_places=3)

    ne_oferte = models.BooleanField(default=False)
    cmimi_ofertes = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)

    stoku_minimal = models.DecimalField(max_digits=10, decimal_places=3, default=5.000)
    data_skadences = models.DateField(null=True, blank=True)
    data_hyrjes = models.DateField(null=True, blank=True)
    data_daljes = models.DateField(null=True, blank=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    krijuar_nga = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    krijuar_me = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkte'

    def clean(self):
        if self.data_hyrjes and self.data_daljes and self.data_daljes < self.data_hyrjes:
            raise ValidationError({
                'data_daljes': "Data e daljes nuk mund te jete para dates se hyrjes."
            })
        if self.njesia_matese != 'KG':
            errors = {}
            if has_decimal_part(self.sasia):
                errors['sasia'] = "Presja dhjetore lejohet vetem per produktet me njesi KG."
            if has_decimal_part(self.stoku_minimal):
                errors['stoku_minimal'] = "Presja dhjetore lejohet vetem per produktet me njesi KG."
            if errors:
                raise ValidationError(errors)

   def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qr_code:
            domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '127.0.0.1:8000')
            protocol = 'https' if os.environ.get('RAILWAY_PUBLIC_DOMAIN') else 'http'
            linku_produktit = f"{protocol}://{domain}/admin/magazina/produkti/{self.id}/change/"
            
            qr = qrcode.make(linku_produktit)
            canvas = BytesIO()
            qr.save(canvas, format='PNG')
            canvas.seek(0)
            filename = get_valid_filename(f'{self.emri}_qr.png')
            self.qr_code.save(filename, File(canvas), save=False)
            super().save(update_fields=['qr_code'])

    def __str__(self):
        return self.emri

class LevizjeStoku(models.Model):
    LLOJI_CHOICES = [
        ('HYRJE', 'Hyrje'),
        ('DALJE', 'Dalje'),
    ]

    produkti = models.ForeignKey(Produkti, on_delete=models.CASCADE, related_name='levizjet')
    perdoruesi = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    lloji = models.CharField(max_length=10, choices=LLOJI_CHOICES)
    sasia = models.DecimalField(max_digits=10, decimal_places=3)
    vlera = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    stoku_pas = models.DecimalField(max_digits=10, decimal_places=3)
    krijuar_me = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-krijuar_me']
        verbose_name = 'Lëvizje stoku'
        verbose_name_plural = 'Lëvizje stoku'

    def __str__(self):
        return f"{self.produkti.emri} - {self.lloji} {self.sasia}"
