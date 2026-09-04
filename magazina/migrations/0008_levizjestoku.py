from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('magazina', '0007_produkti_data_daljes_produkti_data_hyrjes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LevizjeStoku',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lloji', models.CharField(choices=[('HYRJE', 'Hyrje'), ('DALJE', 'Dalje')], max_length=10)),
                ('sasia', models.DecimalField(decimal_places=3, max_digits=10)),
                ('stoku_pas', models.DecimalField(decimal_places=3, max_digits=10)),
                ('krijuar_me', models.DateTimeField(auto_now_add=True)),
                ('perdoruesi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('produkti', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levizjet', to='magazina.produkti')),
            ],
            options={
                'ordering': ['-krijuar_me'],
            },
        ),
    ]
