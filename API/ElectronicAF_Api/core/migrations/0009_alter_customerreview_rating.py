# Generated by Django 4.0.2 on 2022-06-01 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_customerreview_rating_alter_product_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreview',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]
