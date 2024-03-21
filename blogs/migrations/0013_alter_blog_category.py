# Generated by Django 5.0.2 on 2024-03-14 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_blog_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.CharField(choices=[('education', 'Education'), ('music', 'Music'), ('personal', 'Personal'), ('promotions', 'Promotions'), ('travels', 'Travels'), ('others', 'Others')], default='others', max_length=50),
        ),
    ]
