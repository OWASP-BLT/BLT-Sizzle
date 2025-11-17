# Generated for blt-sizzle standalone compatibility

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sizzle', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timelog',
            name='organization',
        ),
        migrations.AddField(
            model_name='timelog',
            name='organization_id',
            field=models.PositiveIntegerField(
                blank=True, 
                help_text='Optional organization reference - safe for standalone usage', 
                null=True
            ),
        ),
        migrations.AddField(
            model_name='timelog',
            name='organization_model',
            field=models.CharField(
                blank=True, 
                help_text='Model path for organization (e.g., \'myapp.Organization\')', 
                max_length=255, 
                null=True
            ),
        ),
    ]