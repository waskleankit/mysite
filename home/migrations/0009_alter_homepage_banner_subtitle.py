# Generated by Django 3.2.12 on 2022-02-22 07:19

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_homepage_banner_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='banner_subtitle',
            field=wagtail.core.fields.RichTextField(),
        ),
    ]
