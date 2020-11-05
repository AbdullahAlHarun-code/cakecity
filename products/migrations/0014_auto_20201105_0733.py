# Generated by Django 3.1.2 on 2020-11-05 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20201105_0410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cakecategory',
            name='image',
        ),
        migrations.AlterField(
            model_name='cakecategory',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cakesizecategory',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='flavour',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='cake_category',
            field=models.CharField(choices=[], max_length=120),
        ),
        migrations.AlterField(
            model_name='product',
            name='create_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='variation',
            name='size',
            field=models.CharField(choices=[], default=None, max_length=120),
        ),
        migrations.AlterField(
            model_name='variation',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
