from flask import render_template, redirect, url_for, flash, request

from app import newsletter_bp
from app.forms import EmailForm, MessageForm


@newsletter_bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('app/home.html')


@newsletter_bp.route('/add-new-email/', methods=['GET', 'POST'])
def add_new_email():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(
                'Новий користувач успішно доданний у список розсилки.',
                category='success'
            )
            return redirect(url_for('newsletter.home'))

    return render_template(
        'app/email_form.html',
        form=form
    )


@newsletter_bp.route('/remove-by-email/', methods=['GET', 'POST'])
def remove_by_email():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(
                'Користувача {} успішно видалено з розсилки.'.format(
                    form.email.data
                ),
                'info'
            )
            return redirect(url_for('newsletter.home'))

    return render_template(
        'app/delete_form.html',
        form=form
    )


@newsletter_bp.route('/compose-message/', methods=['GET', 'POST'])
def compose_message():
    form = MessageForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(
                'Лист успішно відправленно користувачам.',
                'info'
            )
            return redirect(url_for('newsletter.home'))

    return render_template(
        'app/message.html',
        form=form
    )
