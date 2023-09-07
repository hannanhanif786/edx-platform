import mandrill
from celery import shared_task
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

# Mandrill Setup for sending mails
class Mandril:
    """
    For Sending mail through mandril
    """
    ACCOUNT_ACTIVATION_EMAIL = 'complete-registration'
    PASSWORD_RESET_EMAIL = 'password-reset'
    PASSWORD_RESET_COMPLETE = 'password-reset-confirmation'
    VERIFY_CHANGE_USER_EMAIL = 'change-email'
    CHANGE_USER_EMAIL_ALERT = 'email-changed-alert'

    def __init__(self, *args,):
        self.client = MailChimp("87102a871e4fa6ec6dbc367d390756ff-us21", "adeel.anwar")
        self.mandrill_client = mandrill.Mandrill("md-Uog7nlqgFADJ_nH8fCirQA")

    def send_mail(self, data):
        try:
            return self.mandrill_client.messages.send_template(**data)
        except Exception as e:
            print(e)
            return None

    def create_contact(self, user_json):

        try:
            resp = self.client.lists.members.create('1c0ca96c7a', user_json)
        except MailChimpError as error:
            resp = dict(error.args[0])
        return resp

    def update_contact(self, user,  user_json,):

        try:
            resp = self.client.lists.members.update('1c0ca96c7a', user.extended_profile.hubspot_contact_id, user_json)
        except MailChimpError as error:
            resp = dict(error.args[0])
        return resp








# sending Email
@shared_task(bind=True)
def send_mail(self, user_name, email, link=None, temp=None):

    global_merge_vars = []

    if link:
        global_merge_vars = [
            {'name': 'first_name', 'content': user_name},
            {'name': 'activation_link', 'content': link}
        ]

    message = { 'from_email': 'no-reply@philanthropyu.org',
        'from_name': 'CodeFulcrum',
        'to': [{
            'email': email,
            'name': user_name,
            'type': 'to'
        }],
        'global_merge_vars': global_merge_vars,
        }

    data = {
        "template_name" : temp,
        "template_content":[{}],
        "message": message,
    }

    mandril = Mandril()
    desc = mandril.send_mail(data)
    
    