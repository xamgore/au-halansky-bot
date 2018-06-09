from telegram.ext.dispatcher import run_async


def process_chat_msg(cfg):
    msg = cfg.message
    user = msg.from_user
    who = user.full_name + ' ' + user.name
    where = msg.chat.title or who
    subject = '%s___________________________%d|%d' % (where, msg.chat_id, msg.message_id)
    body = '%s\n%s\n%s: %s' % (msg.chat.type, where, who, msg.text_markdown)
    return subject, body


def process_channel_post(cfg):
    msg = cfg.channel_post
    subject = msg.chat.title
    body = '%s\n%s\n%s: %s' % (msg.chat.type, msg.chat.title, msg.author_signature, msg.text_markdown)
    return subject, body


@run_async
def action_send_email(bot, cfg):
    subject, body = process_channel_post(cfg) if cfg.message is None else process_chat_msg(cfg)

    from mailer import send_email_via_yandex
    send_email_via_yandex(subject, body)
    print(subject, body, sep='\n')
