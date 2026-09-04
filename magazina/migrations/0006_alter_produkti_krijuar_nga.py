from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('magazina', '0005_alter_produkti_cmimi_blerjes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produkti',
            name='krijuar_nga',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
