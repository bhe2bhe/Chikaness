# Generated by Django 5.0.2 on 2024-03-04 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_bulletinboard_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bulletinboard',
            name='image',
        ),
    ]
