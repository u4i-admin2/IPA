
from django.conf import settings
from django.db import migrations


def forwards_func(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    db_alias = schema_editor.connection.alias
    (Group.objects.using(db_alias)
        .update_or_create(name=settings.APP_SUPERUSER_GROUP_NAME,
                          defaults={'name': settings.APP_SUPERUSER_GROUP_NAME}))


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]
