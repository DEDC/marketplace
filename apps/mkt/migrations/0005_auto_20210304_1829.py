# Generated by Django 2.2.4 on 2021-03-05 00:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mkt', '0004_auto_20210304_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorias',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_cat', to='mkt.Categorias'),
        ),
    ]
