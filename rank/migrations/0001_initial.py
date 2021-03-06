# Generated by Django 3.2.5 on 2021-08-18 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('company', models.CharField(max_length=50)),
                ('google', models.IntegerField()),
                ('apple', models.IntegerField()),
                ('one', models.IntegerField()),
                ('iconUrl', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'mobile',
            },
        ),
        migrations.CreateModel(
            name='Online',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('company', models.CharField(max_length=50)),
                ('iconUrl', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'online',
            },
        ),
        migrations.CreateModel(
            name='Steam',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('nowCurrent', models.IntegerField()),
                ('fullCurrent', models.IntegerField()),
                ('steamGameKey', models.IntegerField()),
                ('iconUrl', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'steam',
            },
        ),
    ]
