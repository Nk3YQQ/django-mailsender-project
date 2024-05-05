import logging
from datetime import datetime

import pytz
from django.conf import settings
from django.core.mail import send_mail

from mailsender_app.models import Mailing, Client, Attempt

from mailsender_app.services import choose_periodicity, update_mailing_status


logging.basicConfig(filename=f'{settings.CRON_LOGS}', level=logging.DEBUG)


def send_email():
    logging.debug('-----')
    logging.debug('Start sending emails')

    try:
        current_datetime = datetime.now(pytz.utc)
        logging.debug(f'Current datetime: {current_datetime}')

        mailings = Mailing.objects.filter(created_at__lt=current_datetime, ended_at__gt=current_datetime)
        logging.debug(f'Active mailings count: {len(mailings)}')

        for mailing in mailings:
            logging.debug(f'Processing mailing: {mailing.pk}')

            clients_email = mailing.client.values_list('email', flat=True)
            logging.debug(f'Client emails: {list(clients_email)}')

            message = mailing.message
            logging.debug(f'Message title: {message.title}')
            logging.debug(f'Message body: {message.body}')

            e = None

            try:
                send_mail(
                    subject=message.title,
                    message=message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=list(clients_email),
                    fail_silently=False
                )
                logging.debug(f'Message sent successfully: {message.title}')

            except Exception as error:
                e = error
                logging.error(f'Error sending message "{message.title}": {e}')

            for client_email in clients_email:
                client = Client.objects.filter(email=client_email).first()
                Attempt.objects.create(
                    attempt_time=current_datetime,
                    status='Успешно' if not e else 'Не успешно',
                    server_response=str(e) if e else 'Рассылка успешно отправлена',
                    mailing=mailing,
                    client=client
                )
            logging.debug('Attempt records created for all clients')

            choose_periodicity(mailing)
            logging.debug(f'Mailing updated: new created_at - {mailing.created_at}')

            update_mailing_status(mailing, current_datetime)
            logging.debug(f'Mailing status updated: {mailing.status}')

    except Exception as ex:
        logging.error(f'Error in send_email function: {ex}')

    logging.debug('End of sending emails')
    logging.debug('-----')
