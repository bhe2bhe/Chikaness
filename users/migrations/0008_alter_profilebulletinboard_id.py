# Generated by Django 5.0.2 on 2024-03-03 07:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_bulletinboard_liked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilebulletinboard',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
