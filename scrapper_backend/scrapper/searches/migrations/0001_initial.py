# Generated by Django 4.0.2 on 2022-02-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=1000)),
            ],
            options={
                'verbose_name': 'search',
                'verbose_name_plural': 'searches',
            },
        ),
    ]
