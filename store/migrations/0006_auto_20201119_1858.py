# Generated by Django 3.1.2 on 2020-11-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_tshirt_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tshirt',
            name='slug',
            field=models.CharField(default='gibrish', max_length=250, null=True),
        ),
    ]
