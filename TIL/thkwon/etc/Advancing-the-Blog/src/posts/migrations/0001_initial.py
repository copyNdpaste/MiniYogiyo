# Generated by Django 2.2 on 2019-04-09 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='제목')),
                ('content', models.TextField(verbose_name='내용')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='업데이트 시간')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')),
            ],
        ),
    ]
