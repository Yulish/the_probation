# Generated manually to fix migration chain
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('job_training', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]