# Generated by Django 5.1 on 2024-08-13 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
