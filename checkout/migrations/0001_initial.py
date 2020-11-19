# Generated by Django 3.1.2 on 2020-11-19 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0015_auto_20201115_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(editable=False, max_length=32)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=40)),
                ('eircode', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=40)),
                ('address_line_1', models.CharField(max_length=80)),
                ('address_line_2', models.CharField(blank=True, max_length=80)),
                ('county', models.CharField(blank=True, max_length=80)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('item_total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('flavour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.flavour')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.order')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.orderitem')),
            ],
        ),
    ]