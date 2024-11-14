from django.core.management.base import BaseCommand, CommandError
import os
from decouple import config
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

NPM_BIN_PATH = config("NPM_BIN_PATH", cast=str, default=None)
print("NPM_BIN_PATH", NPM_BIN_PATH)
BASE_URL = config("BASE_URL", default='http://127.0.0.1:8000')

BREVO_API_KEY = config("BREVO_API_KEY", cast=str, default=None)

print(f"BREVO_API_KEY: {BREVO_API_KEY}")

class Command(BaseCommand):
    help = 'Send a test email with optional arguments using Brevo'

    def add_arguments(self, parser):
        parser.add_argument('--subject', type=str, help='Email subject (default: "Default Test Email Subject")')
        parser.add_argument('--message', type=str, help='Email message body (default: "This is a default test email message.")')
        parser.add_argument('--from-email', type=str, help='Sender\'s email address (default: value of EMAIL_HOST_USER environment variable)')
        parser.add_argument('--recipient-list', nargs='+', help='List of recipient email addresses (default: ["default-recipient@example.com"])')

    def handle(self, *args, **options):
        subject = options['subject'] or 'Default Test Email Subject'
        message = options['message'] or 'This is a default test email message.'
        from_email = options['from_email'] or os.getenv('EMAIL_HOST_USER')
        recipient_list = options['recipient_list'] or ['angel.kenel@gmail.com']

        # Display the settings
        self.stdout.write("Email Settings:")
        self.stdout.write(f"Subject: {subject}")
        self.stdout.write(f"Message: {message}")
        self.stdout.write(f"From Email: {from_email}")
        self.stdout.write(f"Recipient List: {recipient_list}")

        self.stdout.write("Sending test email...")

        # Configure API key authorization: api-key
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY

        # Create an instance of the API class
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": recipient} for recipient in recipient_list],
            sender={"email": from_email},
            subject=subject,
            html_content=message
        )

        try:
            # Send a transactional email
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
            self.stdout.write(self.style.SUCCESS('Test email sent successfully!'))
        except ApiException as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {e}'))
            raise CommandError('Failed to send email.')

# Run this command using:
# python manage.py test_email --subject "New Subject" --message "New Message" --from-email "your-email@example.com" --recipient-list "recipient@example.com"
