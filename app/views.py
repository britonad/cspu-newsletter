from urllib.parse import urlparse

from app.forms import EmailForm, ListForm, MessageForm
from core import basic_auth
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from utils.common import build_mailgun_url, check_uploaded_files
from utils.mailgun import (
    add_to_mailing_list,
    check_subscription,
    delete_from_mailing_list,
    list_members,
    send_message
)
from werkzeug.datastructures import CombinedMultiDict

newsletter_bp = Blueprint('newsletter', __name__)


@newsletter_bp.route('/', methods=['GET', 'POST'])
@basic_auth.required
def home():
    form = ListForm(request.args)

    address = request.args.get('address')
    limit = request.args.get('limit')
    page = request.args.get('page')

    members = list_members()

    if request.method == 'GET' and all([address, limit, page]):
        if form.validate():
            members = list_members(build_mailgun_url(dict(form.data.items())))
        else:
            flash(form.errors, category='danger')
            return redirect(url_for('newsletter.home'))

    previous = ''.join(['?', urlparse(members['paging']['previous']).query])
    next_p = ''.join(['?', urlparse(members['paging']['next']).query])

    return render_template(
        'app/home.html',
        members=members['items'],
        previous=previous,
        next_p=next_p
    )


@newsletter_bp.route('/add-new-email/', methods=['GET', 'POST'])
@basic_auth.required
def add_new_email():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            exists = add_to_mailing_list(form.email.data.strip())
            if exists:
                flash(
                    'Новий користувач успішно доданний у список розсилки.',
                    category='success'
                )
            else:
                flash(
                    '{} перебуває у списку розсилки'.format(
                        form.email.data.strip()
                    ),
                    'info'
                )
            return redirect(url_for('newsletter.add_new_email'))

    return render_template(
        'app/email_form.html',
        form=form
    )


@newsletter_bp.route('/check-if-exists/', methods=['GET', 'POST'])
@basic_auth.required
def check_if_exists():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            exists = check_subscription(form.email.data.strip())
            if exists.get('message'):
                flash(
                    'Наразі, {} не перебуває у списку розсилки.'.format(
                        form.email.data.strip()
                    ),
                    'info'
                )
            else:
                flash(
                    '{} перебуває у списку розсилки'.format(
                        form.email.data.strip()
                    ),
                    'success'
                )
            return redirect(url_for('newsletter.home'))
    return render_template(
        'app/check_email.html',
        form=form
    )


@newsletter_bp.route('/remove-by-email/', methods=['GET', 'POST'])
@basic_auth.required
def remove_by_email():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            exists = delete_from_mailing_list(form.email.data.strip())
            if not exists.get('member'):
                flash(
                    'Користувача {} немає в списку розсилки.'.format(
                        form.email.data.strip()
                    ),
                    'danger'
                )
            else:
                flash(
                    'Користувача {} успішно видалено з розсилки.'.format(
                        form.email.data.strip()
                    ),
                    'info'
                )
            return redirect(url_for('newsletter.home'))

    return render_template(
        'app/delete_form.html',
        form=form
    )


@newsletter_bp.route('/remove-by-button/<email>/')
@basic_auth.required
def remove_by_button(email):
    exists = delete_from_mailing_list(email)
    if not exists.get('member'):
        flash(
            'Користувача {} немає в списку розсилки.'.format(
                email.strip()
            ),
            'danger'
        )
    else:
        flash(
            'Користувача {} успішно видалено з розсилки.'.format(
                email.strip()
            ),
            'info'
        )
    return redirect(url_for('newsletter.home'))


@newsletter_bp.route('/compose-message/', methods=['GET', 'POST'])
@basic_auth.required
def compose_message():
    form = MessageForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST':
        if form.validate_on_submit():
            result = send_message(
                form.subject.data.strip(),
                form.message.data.strip(),
                check_uploaded_files(form.data.values())
            )
            flash(
                'Лист успішно відправленно користувачам.',
                'info'
            )
            flash(
                'Debug info: {}'.format(result),
                'info'
            )
            return redirect(url_for('newsletter.home'))

    return render_template(
        'app/message.html',
        form=form
    )
