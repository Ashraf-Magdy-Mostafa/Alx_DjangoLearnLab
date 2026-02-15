from django.db import migrations
from taggit.managers import TaggableManager

class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
        ("taggit", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="tags",
            field=TaggableManager(blank=True, help_text="A comma-separated list of tags.", through="taggit.TaggedItem", to="taggit.Tag", verbose_name="Tags"),
        ),
    ]
