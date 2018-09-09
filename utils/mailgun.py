import requests
from unidecode import unidecode

from flask import current_app, render_template

from core.logger import logger


def check_subscription(email):
    """
    Check if an email exists in Mailgun mailing list.

    :param str email: a valid e-mail address
    :return: a dict with subscription status
    :rtype: dict
    """

    response = requests.get(
        'https://api.mailgun.net/v3/lists/{}/members/{}'.format(
            current_app.config['MAILING_LIST'],
            email
        ),
        auth=('api', current_app.config['MAILGUN_API_KEY'])
    ).json()
    logger.info(f'Check subscription of {email}. Response is {response}.')
    return response


def add_to_mailing_list(email):
    """
    Add to a mailing list by a provided e-mail.

    :param str email: a valid e-mail address
    :return: a dict with a subscription status or False
    :rtype: dict or bool
    """

    subscription = check_subscription(email)
    if subscription.get('message'):
        response = requests.post(
            'https://api.mailgun.net/v3/lists/{}/members'.format(
                current_app.config['MAILING_LIST']
            ),
            auth=('api', current_app.config['MAILGUN_API_KEY']),
            data={
                'subscribed': True,
                'address': email
            }
        ).text
        logger.info(
            f'Adding an email {email} to mailing list. Response is {response}.'
        )
        return response
    else:
        return False


def delete_from_mailing_list(email):
    """
    Delete a user from a mailing list by a provided e-mail.

    :param str email: a valid e-mail address
    :return: a dict with a subscription status
    :rtype: dict
    """

    response = requests.delete(
        'https://api.mailgun.net/v3/lists/{}/members/{}'.format(
            current_app.config['MAILING_LIST'],
            email
        ),
        auth=('api', current_app.config['MAILGUN_API_KEY'])
    ).json()
    logger.info(
        f'Deleting {email} from a mailing list. Response is {response}.'
    )
    return response


def list_members(mailgun_url=None):
    """
    List users by a provided Mailgun API url.

    :param mailgun_url: a Mailgun API url with a paging query params
    :return: a list of users
    :rtype: dict
    """

    response = requests.get(
        'https://api.mailgun.net/v3/lists/{}/members/pages'.format(
            current_app.config['MAILING_LIST']
        ) if not mailgun_url else mailgun_url,
        auth=('api', current_app.config['MAILGUN_API_KEY'])
    ).json()
    logger.info(f'Listing users. Reponse is {response}.')
    return response


def send_message(subject, message, attachments):
    """
    Send a message to users that subscribed to a mailing list.

    :param str subject: a subject of a message
    :param str message: a body of a message
    :param list attachments: files to be attached to a message
    :return: a response text
    :rtype: str
    """

    response = requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(
            current_app.config['MAILGUN_DOMAIN_NAME']
        ),
        auth=('api', current_app.config['MAILGUN_API_KEY']),
        files=[
            (
                'attachment',
                (unidecode(attachment.filename), attachment)
            ) for attachment in attachments
        ],
        data={
            'from': 'ЦДПУ ім. В. Винниченка <cspu-newsletter@{}>'.format(
                current_app.config['MAILGUN_DOMAIN_NAME']
            ),
            'to': current_app.config['MAILING_LIST'],
            'subject': subject,
            'html': render_template(
                'mail/template.html',
                subject=subject,
                message=message
            )
        }
    ).text
    logger.info(f'Sending {subject} to users. Response is {response}.')
    return response
