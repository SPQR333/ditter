# Generated by Django 3.2.5 on 2021-07-29 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_alter_avatar_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='picture',
            field=models.ImageField(upload_to='avatars/'),
        ),
    ]
