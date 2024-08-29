# Generated by Django 5.0.7 on 2024-08-28 16:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_subscription'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_users',
            field=models.ManyToManyField(related_name='like_posts', to=settings.AUTH_USER_MODEL, verbose_name='Лайки'),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]