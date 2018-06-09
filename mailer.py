import re
from contextlib import suppress
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
from imbox import Imbox
from config import env

import smtplib as smtp
import threading


def send_email_via_yandex(subject, body=''):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = env['EMAIL_FROM']
    msg['To'] = env['EMAIL_TO']

    # html = """<html><head></head><body>%s</body></html>""" % body
    # part = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    part = MIMEText(body.encode('utf-8'), 'plain', 'utf-8')
    msg.attach(part)

    server = smtp.SMTP_SSL('smtp.yandex.com')
    # server.set_debuglevel(1)
    server.ehlo(env['EMAIL_LOGIN'])
    server.login(env['EMAIL_LOGIN'], env['EMAIL_PASS'])
    server.auth_plain()
    server.sendmail(env['EMAIL_LOGIN'], env['EMAIL_TO'], msg.as_string())
    server.quit()


def fetch_mail(bot, period=10):
    threading.Timer(period, fetch_mail, [bot]).start()
    username = env['EMAIL_LOGIN']
    password = env['EMAIL_PASS']

    with suppress(BaseException):
        with Imbox('imap.yandex.ru', username, password, port=993) as ya:
            for uid, message in ya.messages(unread=True, sent_from=env['EMAIL_TO']):
                with suppress(ValueError):
                    author, numbers, *_ = message.subject.split('_' * 27)
                    chat_id, msg_id, *_ = numbers.split('|')
                    res_msg = bytes("".join(message.body['plain']), 'utf8').decode('unicode_escape')
                    res_msg = ''.join(' ' if s == '\n' else s for s in re.split(r'(\n+)', res_msg))
                    bot.sendMessage(chat_id, res_msg, parse_mode='markdown', reply_to_message_id=msg_id)
                    print('halansky:', res_msg)
                    # print(message.attachments)
                    # message.delete(uid)
                    ya.mark_seen(uid)


fetch_mail(Bot(env['TM_TOKEN']))
