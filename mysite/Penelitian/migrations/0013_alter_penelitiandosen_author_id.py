# Generated by Django 5.1.1 on 2024-11-07 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Penelitian', '0012_penelitiandosen_scopus_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penelitiandosen',
            name='author_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]