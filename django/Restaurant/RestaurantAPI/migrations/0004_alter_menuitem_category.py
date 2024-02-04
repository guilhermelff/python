# Generated by Django 5.0.1 on 2024-02-04 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestaurantAPI', '0003_alter_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='RestaurantAPI.category'),
        ),
    ]
