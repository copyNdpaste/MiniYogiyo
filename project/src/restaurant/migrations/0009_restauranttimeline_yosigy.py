# Generated by Django 2.1 on 2019-06-17 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yosigy', '0004_yosigyticket_status'),
        ('restaurant', '0008_auto_20190613_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='restauranttimeline',
            name='yosigy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='yosigy.Yosigy', verbose_name='요식이 이벤트'),
        ),
    ]
