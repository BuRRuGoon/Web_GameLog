# Generated by Django 3.2.5 on 2021-08-18 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobile',
            name='apple',
        ),
        migrations.RemoveField(
            model_name='mobile',
            name='company',
        ),
        migrations.RemoveField(
            model_name='mobile',
            name='google',
        ),
        migrations.RemoveField(
            model_name='mobile',
            name='iconUrl',
        ),
        migrations.RemoveField(
            model_name='mobile',
            name='one',
        ),
        migrations.RemoveField(
            model_name='mobile',
            name='title',
        ),
        migrations.RemoveField(
            model_name='online',
            name='company',
        ),
        migrations.RemoveField(
            model_name='online',
            name='iconUrl',
        ),
        migrations.RemoveField(
            model_name='online',
            name='title',
        ),
        migrations.RemoveField(
            model_name='steam',
            name='fullCurrent',
        ),
        migrations.RemoveField(
            model_name='steam',
            name='iconUrl',
        ),
        migrations.RemoveField(
            model_name='steam',
            name='nowCurrent',
        ),
        migrations.RemoveField(
            model_name='steam',
            name='steamGameKey',
        ),
        migrations.RemoveField(
            model_name='steam',
            name='title',
        ),
        migrations.AlterField(
            model_name='mobile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='online',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='steam',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
