# Generated by Django 4.0.2 on 2022-05-23 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_image_tumbnail_image_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='os',
            field=models.CharField(blank=True, max_length=55),
        ),
    ]