# Generated by Django 2.2 on 2020-05-27 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200528_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('POD', 'POD'), ('MANUF', 'MANUF'), ('BULK', 'BULK')], max_length=100, null=True),
        ),
    ]
