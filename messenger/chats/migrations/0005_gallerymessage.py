# Generated by Django 5.0.7 on 2024-09-01 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_chat_group_chat_admin_chat_group_chat_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='photos/chats/%Y/%m/%d/', verbose_name='Фото')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='chats.message')),
            ],
        ),
    ]
