# Generated by Django 4.2.3 on 2023-10-16 19:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserPages', '0009_remove_comments_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.ManyToManyField(blank=True, related_name='shared_posts_comments', to='UserPages.comments')),
                ('original_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserPages.usercontent')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='shared_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shared_comments', to='UserPages.sharedpost'),
        ),
    ]
