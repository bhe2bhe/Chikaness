# Generated by Django 5.0.2 on 2024-03-25 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0018_alter_blog_image2_caption_alter_blog_image3_caption_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(default='blog-default.jpeg', upload_to='blog_pics'),
        ),
    ]
