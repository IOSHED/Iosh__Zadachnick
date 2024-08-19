# Generated by Django 5.1 on 2024-08-19 09:52

import accounts.lib.path
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.TextField(max_length=255, null=True)),
                ('surname', models.TextField(max_length=255, null=True)),
                ('chat_telegram_id', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('icon32', models.ImageField(default='default/user_icon_32.png', upload_to=accounts.lib.path.user_directory_path)),
                ('icon64', models.ImageField(default='default/user_icon_64.png', upload_to=accounts.lib.path.user_directory_path)),
                ('birthday_at', models.DateField(null=True)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_email_verification', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
