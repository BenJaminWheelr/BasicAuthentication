# Generated by Django 5.1.2 on 2024-10-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('passwordHash', models.TextField()),
            ],
        ),
    ]
