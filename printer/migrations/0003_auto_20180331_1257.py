# Generated by Django 2.0.3 on 2018-03-31 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0002_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AlterField(
            model_name='printer',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
