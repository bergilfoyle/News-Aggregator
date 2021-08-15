# Generated by Django 3.2.5 on 2021-08-14 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.CharField(default='_', max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(default='_', help_text='Enter the summary', max_length=200),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(default='_', max_length=200),
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(default='_', max_length=200),
        ),
        migrations.AlterField(
            model_name='source',
            name='url',
            field=models.CharField(default='_', max_length=200),
        ),
    ]
