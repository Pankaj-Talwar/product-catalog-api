# Generated by Django 5.0.6 on 2024-08-27 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
