from django.db import migrations, models
import magazina.models


class Migration(migrations.Migration):

    dependencies = [
        ('magazina', '0006_alter_produkti_krijuar_nga'),
    ]

    operations = [
        migrations.AddField(
            model_name='produkti',
            name='data_daljes',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='produkti',
            name='data_hyrjes',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='produkti',
            name='pershkrimi',
            field=models.TextField(blank=True, default='', validators=[magazina.models.validate_max_50_words]),
        ),
    ]
