# Generated by Django 5.0.4 on 2024-05-22 20:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_alter_event_event_categories_alter_event_event_tags'),
        ('misc', '0001_initial'),
        ('post', '0003_comment_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='misc.category'),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AlterField(
            model_name='post',
            name='post_tags',
            field=models.ManyToManyField(blank=True, to='misc.tag'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
