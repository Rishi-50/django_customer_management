# Generated by Django 5.0.7 on 2025-03-12 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='note',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
