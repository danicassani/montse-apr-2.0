# Generated by Django 4.2.2 on 2023-06-25 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_alter_phrase_reviewer_suggestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion',
            name='reviewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='suggestion_reviewer', to='db.user'),
        ),
    ]
