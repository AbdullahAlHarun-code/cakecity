# Generated by Django 3.1.2 on 2020-10-23 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20201023_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tier',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3"'), ('4', '4"'), ('5', '5"'), ('6', '6"')], default='1', max_length=120),
        ),
        migrations.AlterField(
            model_name='variation',
            name='size',
            field=models.CharField(choices=[('8', '8'), ('10', '10'), ('12', '12'), ('6"/8"', '6"/8"'), ('6"/10"', '6"/10"'), ('8"/12"', '8"/12"'), ('8"/10"', '8"/10"')], default=None, max_length=120),
        ),
    ]
