from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0002_movie_director_alter_movie_rating_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="tittle",
            new_name="title",
        ),
        migrations.AlterModelOptions(
            name="movie",
            options={"ordering": ["title"]},
        ),
    ]
