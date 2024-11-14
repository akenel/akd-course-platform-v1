from django.core.management.base import BaseCommand, CommandError
import requests
import json
from decouple import config
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Send a test email campaign using Brevo'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help='Campaign name (default: "Campaign sent via the API")')
        parser.add_argument('--subject', type=str, help='Email subject (default: "My subject")')
        parser.add_argument('--sender-name', type=str, help='Sender name (default: "From name")')
        parser.add_argument('--sender-email', type=str, help='Sender email address (default: "myfromemail@mycompany.com")')
        parser.add_argument('--html-content', type=str, help='HTML content of the email (default: "Congratulations! You successfully sent this example campaign via the Brevo API.")')
        parser.add_argument('--list-ids', nargs='+', type=int, help='List of recipient list IDs (default: [2, 7])')
        parser.add_argument('--scheduled-at', type=str, help='Scheduled time for sending the email (default: 10 seconds in the future)')

    def handle(self, *args, **options):
        BREVO_API_KEY = config("BREVO_API_KEY", cast=str, default=None)
        if not BREVO_API_KEY:
            raise CommandError('BREVO_API_KEY is not set in the environment variables.')

        EMAIL_SENDER = config("EMAIL_SENDER", cast=str, default=None)
        EMAIL_TARGET = config("EMAIL_TARGET", cast=str, default=None)
       
        if options['sender_email'] is None:
            options['sender_email'] = EMAIL_SENDER
        if options['list_ids'] is None:
            options['list_ids'] = [EMAIL_TARGET]
        if options['sender_name'] is None:
            options['sender_name'] = EMAIL_SENDER
        if options['scheduled_at'] is None:
            options['scheduled_at'] = (datetime.utcnow() + timedelta(seconds=20)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            scheduled_datetime = datetime.strptime(options['scheduled_at'], '%Y-%m-%d %H:%M:%S')
            if scheduled_datetime <= datetime.utcnow():
                raise CommandError('Scheduled date should be in the future.')

        if options['html_content'] is None:
            options['html_content'] = "Congratulations! You successfully sent this example campaign via the Brevo API."
        if options['subject'] is None:
            options['subject'] = "My subject"
        if options['name'] is None:
            options['name'] = "Campaign sent via the API"

        campaign_data = {
            "name": options['name'],
            "subject": options['subject'],
            "sender": {
                "name": options['sender_name'],
                "email": options['sender_email']
            },
            "type": "classic",
            "htmlContent": options['html_content'],
            "recipients": {
                "listIds": options['list_ids']
            },
            "scheduledAt": options['scheduled_at']
        }

        headers = {
            'api-key': BREVO_API_KEY,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            'https://api.brevo.com/v3/emailCampaigns',
            headers=headers,
            data=json.dumps(campaign_data)
        )

        if response.status_code == 201:
            self.stdout.write(self.style.SUCCESS('Campaign created successfully!'))
            self.stdout.write(json.dumps(response.json(), indent=4))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to create campaign: {response.status_code}'))
            self.stdout.write(response.text)

# Run this command using:
# python manage.py brevo_email_test --name "New Campaign" --subject "New Subject" --sender-name "Your Name" --sender-email "yourname@example.com" --html-content "Your HTML content" --list-ids 1 2 3 --scheduled-at "2024-11-14 23:59:59"
