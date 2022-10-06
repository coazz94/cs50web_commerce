# Generated by Django 4.1.2 on 2022-10-06 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_name_listing_title_alter_listing_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='url',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(default='not_defined', max_length=15),
        ),
        migrations.AlterField(
            model_name='listing',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]