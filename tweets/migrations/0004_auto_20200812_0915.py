# Generated by Django 3.0 on 2020-08-12 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0003_auto_20200811_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='RETweeT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=250, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('org_tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweets.Tweet')),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='retweet_comment',
            field=models.ManyToManyField(related_name='retweets', through='tweets.RETweeT', to=settings.AUTH_USER_MODEL),
        ),
    ]
