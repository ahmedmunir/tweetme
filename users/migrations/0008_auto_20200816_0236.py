# Generated by Django 3.0 on 2020-08-16 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200816_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='image',
            field=models.ImageField(default='0.jpg', upload_to='profile_pics/'),
        ),
    ]
