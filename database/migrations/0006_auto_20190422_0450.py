# Generated by Django 2.2 on 2019-04-22 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_comment_creditcard_filter_image_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='filtered_versions',
        ),
        migrations.RemoveField(
            model_name='image',
            name='original_image',
        ),
    ]