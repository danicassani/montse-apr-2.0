# Generated by Django 4.2.2 on 2023-06-25 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_rename_text_suggestion_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='excercise',
            old_name='name',
            new_name='title',
        ),
    ]
