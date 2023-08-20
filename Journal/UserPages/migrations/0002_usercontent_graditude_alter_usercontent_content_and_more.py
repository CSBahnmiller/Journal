# Generated by Django 4.2.3 on 2023-08-20 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserPages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercontent',
            name='graditude',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='usercontent',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='usercontent',
            name='mood',
            field=models.CharField(choices=[('Happy 😃', 'Happy 😃'), ('Peaceful 😃', 'Peaceful 😃'), ('Sad 😢', 'Sad 😢'), ('Mad 😤', 'Mad 😤'), ('Anxious 😰', 'Anxious 😰'), ('Depressed 😓', 'Depressed 😓'), ('No Mood 😑', 'No Mood 😑'), ('Angry 😤', 'Angry 😤'), ('Excited 😃', 'Excited 😃'), ('Silly 😋', 'Silly 😋'), ('Curious 🦝', 'Curious 🦝'), ('Insightful 🤔', 'Insightful 🤔')], default='Happy 😃', max_length=20, verbose_name='Current Mood:'),
        ),
    ]
