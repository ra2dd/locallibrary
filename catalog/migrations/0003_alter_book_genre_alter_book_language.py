# Generated by Django 4.2 on 2023-05-01 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language_book_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Select genre for this book.', to='catalog.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(help_text='Enter the Language for the book.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]
