# Generated by Django 5.0.2 on 2024-03-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_profilebulletinboard_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilebulletinboard',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
