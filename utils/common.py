from urllib.parse import urlencode

from flask import current_app


def build_mailgun_url(query_data):
    """
    Build a proper URL for paging Mailgun API request.

    :param dict query_data: a dict to build a query string
    :return: a Mailgun paging URL
    :rtype: str
    """

    mailgun_url = '{}/lists/{}/members/pages'
    mailgun_url = mailgun_url.format(
        current_app.config['MAILGUN_BASE_URL'],
        current_app.config['MAILING_LIST']
    )
    mailgun_url = ''.join([mailgun_url, '?', urlencode(query_data)])

    return mailgun_url


def check_uploaded_files(data):
    """
    Check if submitted attachments have a filename field. It needs to attach
    proper files to a message.

    :param dict_values data: a list of attachments
    :return: a list of proper FileStorage files
    :rtype: list
    """

    files = []
    for field in data:
        if hasattr(field, 'filename'):
            if field.filename:
                files.append(field)

    return files
