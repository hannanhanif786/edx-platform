# Generated by Django 3.2.20 on 2023-08-22 11:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import lms.djangoapps.onboarding.models
import model_utils.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('alphabetic_code', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('minor_units', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='EnglishProficiency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='FocusArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='FunctionArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='OperationLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('label', models.CharField(db_index=True, max_length=255)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('unclaimed_org_admin_email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('url', models.URLField(blank=True, max_length=255, null=True, validators=[lms.djangoapps.onboarding.models.SchemaOrNoSchemaURLValidator])),
                ('founding_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('registration_number', models.CharField(blank=True, max_length=30, null=True)),
                ('org_type', models.CharField(blank=True, max_length=10, null=True)),
                ('level_of_operation', models.CharField(blank=True, max_length=10, null=True)),
                ('focus_area', models.CharField(blank=True, max_length=10, null=True)),
                ('total_employees', models.CharField(blank=True, max_length=10, null=True)),
                ('is_organization_registered', models.CharField(blank=True, max_length=20, null=True, verbose_name='Is Organization Registered as 501c3?')),
                ('alternate_admin_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('has_affiliated_partner', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrgSector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='PartnerNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=255)),
                ('is_partner_affiliated', models.BooleanField(default=False)),
                ('show_opt_in', models.BooleanField(default=False)),
                ('affiliated_name', models.CharField(blank=True, max_length=32, null=True)),
                ('program_name', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='RoleInsideOrg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TotalEmployee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(null=True, unique=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('label', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='UserExtendedProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('country_of_employment', models.CharField(max_length=255, null=True)),
                ('not_listed_gender', models.CharField(blank=True, max_length=255, null=True)),
                ('city_of_employment', models.CharField(max_length=255, null=True)),
                ('english_proficiency', models.CharField(max_length=10, null=True)),
                ('start_month_year', models.CharField(max_length=100, null=True)),
                ('role_in_org', models.CharField(max_length=10, null=True)),
                ('hours_per_week', models.PositiveIntegerField(default=0, null=True, validators=[django.core.validators.MaxValueValidator(168)], verbose_name='Typical Number of Hours Worked per Week*')),
                ('is_interests_data_submitted', models.BooleanField(default=False)),
                ('is_organization_metrics_submitted', models.BooleanField(default=False)),
                ('is_first_learner', models.BooleanField(default=False)),
                ('is_alquity_user', models.BooleanField(default=False)),
                ('hear_about_philanthropyu', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('hear_about_philanthropy_partner', 'A Philanthropy University Partner (Global Giving, +Acumen or another)'), ('hear_about_colleague_same_organization', 'A Colleague From My Organization'), ('hear_about_friend_new_organization', 'A Friend Or Colleague (Not From My Organization)'), ('hear_about_internet_search', 'An Internet Search'), ('hear_about_linkedIn_advertisement', 'A LinkedIn Advertisement'), ('hear_about_facebook_advertisement', 'A Facebook Advertisement'), ('hear_about_twitter_not_colleague', 'Twitter (Not From A Colleague)')], max_length=255)),
                ('function_areas', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('function_strategy_planning', 'Strategy and planning'), ('function_leadership_governance', 'Leadership and governance'), ('function_program_design', 'Program design and development'), ('function_measurement_eval', 'Measurement, evaluation, and learning'), ('function_stakeholder_engagement', 'External relations and partnerships'), ('function_human_resource', 'Human resource management'), ('function_financial_management', 'Financial management'), ('function_fundraising', 'Fundraising and resource mobilization'), ('function_marketing_communication', 'Marketing, communications, and PR'), ('function_system_tools', 'Systems, tools, and processes')], max_length=269)),
                ('interests', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('interest_strategy_planning', 'Strategy and planning'), ('interest_leadership_governance', 'Leadership and governance'), ('interest_program_design', 'Program design and development'), ('interest_measurement_eval', 'Measurement, evaluation, and learning'), ('interest_stakeholder_engagement', 'External relations and partnerships'), ('interest_human_resource', 'Human resource management'), ('interest_financial_management', 'Financial management'), ('interest_fundraising', 'Fundraising and resource mobilization'), ('interest_marketing_communication', 'Marketing, communications, and PR'), ('interest_system_tools', 'Systems, tools, and processes')], max_length=269)),
                ('learners_related', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('learners_same_region', 'Learners from my region or country'), ('learners_similar_oe_interest', 'Learners interested in same areas of organization effectiveness'), ('learners_similar_org', 'Learners working for similar organizations'), ('learners_diff_who_are_different', 'Learners who are different from me')], max_length=102)),
                ('goals', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('goal_contribute_to_org', 'Help improve my organization'), ('goal_gain_new_skill', 'Develop new skills'), ('goal_improve_job_prospect', 'Get a job'), ('goal_relation_with_other', 'Build relationships with other nonprofit leaders')], max_length=93)),
                ('hubspot_contact_id', models.CharField(max_length=20, null=True)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extended_profile', to='onboarding.organization')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='extended_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('linkedin_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationPartner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner', models.CharField(max_length=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_partners', to='onboarding.organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationMetricUpdatePrompt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latest_metric_submission', models.DateTimeField()),
                ('year', models.BooleanField(default=False)),
                ('year_month', models.BooleanField(default=False)),
                ('year_three_month', models.BooleanField(default=False)),
                ('year_six_month', models.BooleanField(default=False)),
                ('remind_me_later', models.NullBooleanField()),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_metrics_update_prompts', to='onboarding.organization')),
                ('responsible_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_metrics_update_prompts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('actual_data', models.NullBooleanField(choices=[(0, 'Estimated - My answers are my best guesses based on my knowledge of the organization'), (1, "Actual - My answers come directly from my organization's official documentation")])),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('total_clients', models.PositiveIntegerField(blank=True, null=True)),
                ('total_employees', models.PositiveIntegerField(blank=True, null=True)),
                ('local_currency', models.CharField(blank=True, max_length=10, null=True)),
                ('total_revenue', models.BigIntegerField(blank=True, null=True)),
                ('total_donations', models.BigIntegerField(blank=True, null=True)),
                ('total_expenses', models.BigIntegerField(blank=True, null=True)),
                ('total_program_expenses', models.BigIntegerField(blank=True, null=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_metrics', to='onboarding.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_metrics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationAdminHashKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('suggested_admin_email', models.EmailField(max_length=254)),
                ('is_hash_consumed', models.BooleanField(default=False)),
                ('activation_hash', models.CharField(max_length=32)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggested_admins', to='onboarding.organization')),
                ('suggested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MetricUpdatePromptRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('click', models.CharField(choices=[('RML', 'Remind Me Later'), ('TMT', 'Take Me There'), ('NT', "No Thanks, I'm Not Interested")], db_index=True, max_length=3, null=True)),
                ('prompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics_update_prompt_records', to='onboarding.organizationmetricupdateprompt')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GranteeOptIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreed', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization_partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grantee_opt_in', to='onboarding.organizationpartner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grantee_opt_in', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('linkedin_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.CharField(blank=True, max_length=255, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailPreference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('opt_in', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='email_preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('linkedin_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('degree_name', models.CharField(blank=True, max_length=255, null=True)),
                ('start_month_year', models.DateField(blank=True, null=True)),
                ('end_month_year', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='education', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
