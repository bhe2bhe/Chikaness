# Generated by Django 4.2.4 on 2024-02-23 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profilebulletinboard_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilebulletinboard',
            name='profile',
        ),
    ]
