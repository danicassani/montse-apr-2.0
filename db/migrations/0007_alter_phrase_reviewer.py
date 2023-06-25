# Generated by Django 4.2.2 on 2023-06-25 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_suggestion_resolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phrase',
            name='reviewer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='phrase_reviewer', to='db.user'),
        ),
    ]
