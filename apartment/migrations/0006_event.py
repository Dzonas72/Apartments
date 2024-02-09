# Generated by Django 5.0.1 on 2024-01-30 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0005_room_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
    ]