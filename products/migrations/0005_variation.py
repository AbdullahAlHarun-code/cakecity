# Generated by Django 3.1.2 on 2020-11-09 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20201109_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[(1, '6"'), (2, '8"'), (3, '10"'), (4, '12"'), (5, '6"/8"'), (6, '6"/10"'), (7, '8"/10"'), (9, '4"/6"/8"'), (10, '6"/8"/10"'), (8, '8"/12"'), (11, '4"/6"/8"/10"'), (12, '6"/8"/10"/12"')], default=None, max_length=120)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=100, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
