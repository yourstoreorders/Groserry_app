from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, template, data):
    app = current_app._get_current_object()

    msg = Message(subject, recipients=[app.config['ORDER_MAIL_RECEIVER']])


    # msg.body = "New Order From" + template
    msg.html = render_template(template + '.html', data=data)

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    return thr