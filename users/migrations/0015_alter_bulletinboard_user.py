# Generated by Django 5.0.2 on 2024-03-04 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_bulletinboard_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulletinboard',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
