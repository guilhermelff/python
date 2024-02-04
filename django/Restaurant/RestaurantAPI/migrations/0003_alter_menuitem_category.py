# Generated by Django 5.0.1 on 2024-02-04 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantAPI', '0002_category_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='RestaurantAPI.category'),
        ),
    ]
