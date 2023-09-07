from celery import shared_task
from django.contrib.auth.models import User
from lms.djangoapps.onboarding.models import UserExtendedProfile
from common.djangoapps.util.lib.mandril import Mandril
from common.djangoapps.util.lib.hubspot_client.helpers import prepare_user_data_for_hubspot_contact_creation

@shared_task(bind=True)
def task_send_hubspot_email(self, data):
    """
    Task to send email using MailChimp Client.
    """
    global_merge_vars = []
    template_name = data['emailId']
    template_content = [{}]
    for key, value in data['customProperties'].items():
        global_merge_vars.append({'name': key, 'content': value})
    message = {
        'to': [{
            'email': data['message']['to'],
            'type': 'to'
        }],
        'global_merge_vars': global_merge_vars
    }
    email_data = dict(template_name=template_name, template_content=template_content, message=message)
    Mandril().send_mail(email_data)

@shared_task(bind=True)
def task_create_or_update_hubspot_contact(self, user_email, user_json, is_contact_created=False):
    """
    Task to Create or Update marketing contact on MailChimp.

    Following steps are being performed:
    1. Update contact on MailChimp if we have the MailChimp id of contact.
    2. If contact is not synced before then try to create contact on MailChimp.
        i. If contact creation is successful, save the MailChimp Contact id.
        ii. If we get an error that contact already exists with the email then save the MailChimp Contact id and make an
            update request.

    Arguments:
        user_email (str): Email of user.
        user_json (dict): Data for MailChimp request.
        is_contact_created (bool): Is contact already synced with MailChimp.
    """

    user = User.objects.filter(email=user_email).first()
    if not user:
        return

    properties = user_json.get('properties')
    edx_marketing_opt_in = properties.get('edx_marketing_opt_in', 'cleaned')
    edx_marketing_opt_in = 'subscribed' if edx_marketing_opt_in == 'TRUE' else edx_marketing_opt_in

    data = {
        'email_address': properties.get('email'),
        'status': edx_marketing_opt_in if edx_marketing_opt_in != 'subscribed' else 'cleaned',
    }

    client = Mandril()
    if is_contact_created:

        client.update_contact(user, data)
        return

    data['merge_fields'] = {
        'USERNAME': properties.get('edx_username'),
        'FULLNAME': properties.get('edx_full_name'),
        'DATEREGIS': properties.get('date_registered'),
        # 'LANGUAGE': properties.get('edx_language'),
        # 'COUNTRY': properties.get('edx_country'),
        # 'CITY': properties.get('edx_city'),
        'ENROLLMENT': properties.get('edx_enrollments'),
        'EMTSHRTIDS': properties.get('edx_enrollments_short_ids'),
    }
    contact = client.create_contact(data)
    if contact.get('id'):
        hubspot_contact_id = contact.get('id')
        UserExtendedProfile.objects.update_or_create(user=user, defaults={'hubspot_contact_id': hubspot_contact_id})

    elif contact.get('status') == 400:
        message = contact.get('detail')
        if contact.get('title') == 'Member Exists':
            hubspot_contact_id = contact.get('instance')
            UserExtendedProfile.objects.update_or_create(user=user, defaults={'hubspot_contact_id': hubspot_contact_id})
            client.update_contact(user, user_json)

@shared_task(bind=True)
def task_update_org_details_at_hubspot(self, org_label, org_type, work_area, org_id):
    """
    Update the details of the organization associated with the org_id

    Arguments:
        org_id (int): id of the target organization
        org_label (str): Label of the organization to update
        org_type (str): Type of the organization to update
        work_area (str): Work area of the organization to update
    """

    extended_profiles = UserExtendedProfile.objects.filter(organization_id=org_id).select_related('user')
    user_json = {
        'properties': {
            'edx_organization': org_label,
            'edx_organization_type': org_type,
            'edx_area_of_work': work_area
        }
    }

    for extended_profile in extended_profiles:
        user = extended_profile.user
        if not extended_profile.hubspot_contact_id:
            user_json = prepare_user_data_for_hubspot_contact_creation(extended_profile.user)

        task_create_or_update_hubspot_contact.delay(
            user.email, user_json, bool(extended_profile.hubspot_contact_id)
        )