# Generated by Django 5.0.3 on 2024-05-26 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Train', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='train',
            name='totalTicket',
            field=models.IntegerField(blank=True, default=20, null=True),
        ),
        migrations.DeleteModel(
            name='addTicket',
        ),
    ]
