# Generated by Django 4.2.2 on 2023-06-25 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phrase',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='phrase_reviewer', to='db.user'),
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=2000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suggestion_reviewer', to='db.user')),
                ('suggester', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='suggester', to='db.user')),
            ],
        ),
    ]
