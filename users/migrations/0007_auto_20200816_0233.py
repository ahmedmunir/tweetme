# Generated by Django 3.0 on 2020-08-16 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_newuser_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
