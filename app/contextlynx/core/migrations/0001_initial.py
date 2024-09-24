# Generated by Django 5.1.1 on 2024-09-24 06:49

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import pgvector.django.indexes
import pgvector.django.vector
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('icon', models.CharField(max_length=16, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('latest_node_embedding_calculated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NodeEmbedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embedding_model', models.CharField(max_length=50)),
                ('embedding_vector', pgvector.django.vector.VectorField(dimensions=16)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('predicted', models.BooleanField(default=False)),
                ('from_object_id', models.PositiveIntegerField()),
                ('to_object_id', models.PositiveIntegerField()),
                ('similarity', models.FloatField(null=True)),
                ('from_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_edges', to='contenttypes.contenttype')),
                ('to_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_edges', to='contenttypes.contenttype')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
        migrations.CreateModel(
            name='WordEmbedding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('embedding_model', models.CharField(max_length=50)),
                ('embedding_vector', pgvector.django.vector.VectorField(dimensions=768)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
            ],
        ),
        migrations.CreateModel(
            name='NodeTopic',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('disabled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512)),
                ('data_type', models.CharField(choices=[('OTHER', 'Other'), ('CONCEPT', 'Concept'), ('PERSON', 'Person'), ('ORGANIZATION', 'Organization'), ('LOCATION', 'Location'), ('DATE', 'Date'), ('EVENT', 'Event'), ('PRODUCT', 'Product'), ('WORK_OF_ART', 'Work Of Art'), ('LAW', 'Law'), ('LANGUAGE', 'Language'), ('QUANTITY', 'Quantity'), ('TIME', 'Time'), ('URL', 'Url'), ('EMAIL', 'Email'), ('PHONE_NUMBER', 'Phone Number'), ('NATIONALITY', 'Nationality'), ('RELIGION', 'Religion'), ('VEHICLE', 'Vehicle'), ('ANIMAL', 'Animal'), ('PLANT', 'Plant'), ('MEDICAL_CONDITION', 'Medical Condition'), ('SPORTS_TEAM', 'Sports Team'), ('INDUSTRY', 'Industry'), ('COMPANY', 'Company')], default='OTHER', max_length=20)),
                ('language', models.CharField(max_length=10)),
                ('node_embedding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topic_node_embeddings', to='core.nodeembedding')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
                ('word_embedding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topic_word_embeddings', to='core.wordembedding')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NodeNote',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('disabled', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('language', models.CharField(max_length=10)),
                ('icon', models.CharField(default='🗒', max_length=16)),
                ('title', models.CharField(max_length=255)),
                ('short_summary', models.TextField(null=True)),
                ('data_input', models.TextField()),
                ('data_raw', models.TextField()),
                ('data_type', models.CharField(choices=[('TEXT', 'Text'), ('WEBPAGE', 'Webpage')], max_length=10)),
                ('data_sanitized_md', models.TextField()),
                ('node_embedding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note_node_embeddings', to='core.nodeembedding')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.project')),
                ('word_embedding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='note_word_embeddings', to='core.wordembedding')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='nodeembedding',
            index=pgvector.django.indexes.HnswIndex(ef_construction=128, fields=['embedding_vector'], m=32, name='node_embedding_vector', opclasses=['vector_cosine_ops']),
        ),
        migrations.AddIndex(
            model_name='wordembedding',
            index=pgvector.django.indexes.HnswIndex(ef_construction=128, fields=['embedding_vector'], m=32, name='word_embedding_vector', opclasses=['vector_cosine_ops']),
        ),
    ]
