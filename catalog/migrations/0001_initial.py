# Generated by Django 4.2.11 on 2024-04-17 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "date_of_death",
                    models.DateField(blank=True, null=True, verbose_name="Died"),
                ),
            ],
            options={
                "ordering": ["last_name", "first_name"],
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "summary",
                    models.TextField(
                        help_text="Enter a brief description of the book",
                        max_length=1000,
                    ),
                ),
                (
                    "isbn",
                    models.CharField(
                        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
                        max_length=13,
                        unique=True,
                        verbose_name="ISBN",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookInstance",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unique ID for this particular book across whole library",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("imprint", models.CharField(max_length=200)),
                ("due_back", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("m", "Maintenance"),
                            ("o", "On loan"),
                            ("a", "Available"),
                            ("r", "Reserved"),
                        ],
                        default="m",
                        help_text="Book availability",
                        max_length=1,
                    ),
                ),
            ],
            options={
                "ordering": ["due_back"],
                "permissions": (("can_mark_returned", "Set book as returned"),),
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Enter a book genre (e.g. Science Fiction, French Poetry, etc.)",
                        max_length=200,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",
                        max_length=200,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MyModelName",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "my_field_name",
                    models.CharField(help_text="Field documentation", max_length=20),
                ),
            ],
            options={
                "ordering": ["-my_field_name"],
            },
        ),
        migrations.AddConstraint(
            model_name="language",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                name="language_name_case_insensitive_unique",
                violation_error_message="Language already exists (case insensitive match)",
            ),
        ),
        migrations.AddConstraint(
            model_name="genre",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                name="genre_name_case_insensitive_unique",
                violation_error_message="Genre already exists (case insensitive match)",
            ),
        ),
        migrations.AddField(
            model_name="bookinstance",
            name="book",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="catalog.book",
            ),
        ),
        migrations.AddField(
            model_name="bookinstance",
            name="borrower",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="catalog.author",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="genre",
            field=models.ManyToManyField(
                help_text="Select a genre for this book", to="catalog.genre"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="language",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.language",
            ),
        ),
    ]
