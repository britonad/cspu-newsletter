import requests

from flask import render_template

from core import app
from utils.common import parse_url


def check_subscription(email):
    return requests.get(
        'https://api.mailgun.net/v3/lists/{}/members/{}'.format(
            app.config['MAILING_LIST'],
            email
        ),
        auth=('api', app.config['MAILGUN_API_KEY'])
    ).json()


def add_to_mailing_list(email):
    exists = check_subscription(email)
    if exists.get('message'):
        return requests.post(
            'https://api.mailgun.net/v3/lists/{}/members'.format(
                app.config['MAILING_LIST']
            ),
            auth=('api', app.config['MAILGUN_API_KEY']),
            data={
                'subscribed': True,
                'address': email
            }
        ).text
    else:
        return False


def delete_from_mailing_list(email):
    return requests.delete(
        'https://api.mailgun.net/v3/lists/{}/members/{}'.format(
            app.config['MAILING_LIST'],
            email
        ),
        auth=('api', app.config['MAILGUN_API_KEY'])
    ).json()


def list_members():
    return requests.get(
        'https://api.mailgun.net/v3/lists/{}/members/pages'.format(
            app.config['MAILING_LIST']
        ),
        auth=('api', app.config['MAILGUN_API_KEY'])
    ).json()


def send_message(subject, message, url):
    return requests.post(
        'https://api.mailgun.net/v3/{}/messages'.format(
            app.config['MAILGUN_DOMAIN_NAME']
        ),
        auth=('api', app.config['MAILGUN_API_KEY']),
        data={
            'from': 'cspu-newsletter@{}'.format(
                app.config['MAILGUN_DOMAIN_NAME']
            ),
            'to': app.config['MAILING_LIST'],
            'subject': subject,
            'html': render_template(
                'mail/template.html',
                subject=subject,
                message=message,
                logo_url='{}/static/img/cspu.png'.format(parse_url(url))
            )
        }
    ).text
