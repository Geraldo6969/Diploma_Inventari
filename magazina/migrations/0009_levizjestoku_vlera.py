from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazina', '0008_levizjestoku'),
    ]

    operations = [
        migrations.AddField(
            model_name='levizjestoku',
            name='vlera',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=12),
        ),
    ]
