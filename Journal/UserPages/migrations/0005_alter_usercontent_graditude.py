# Generated by Django 4.2.3 on 2023-09-02 23:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserPages', '0004_usercontent_content_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontent',
            name='graditude',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]