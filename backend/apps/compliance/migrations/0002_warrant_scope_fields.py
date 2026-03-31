from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('compliance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='warrant',
            name='authorized_scope',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='warrant',
            name='proportionality_notes',
            field=models.TextField(blank=True),
        ),
    ]
