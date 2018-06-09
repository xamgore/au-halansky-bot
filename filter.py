from telegram.ext import BaseFilter, Filters
from config import env


class InteractionWithBot(BaseFilter):
    """
    This filter keeps the following types of messages:

    * A reply to the bot's message
    * A message with `@mention`
    * A private conversation message
    * A post in AU17 channel
    """
    __send_all_messages = False


    def filter(self, msg):
        mentions = [e for e in msg.entities if e.type == e.MENTION]
        logins = [msg.text[m.offset + 1:m.offset + m.length] for m in mentions]
        is_mention = (env['BOT_LOGIN'] in logins) or (env['BOT_NAME'] in logins)

        is_reply = msg.reply_to_message and msg.reply_to_message.from_user.username == env['BOT_LOGIN']
        is_channel = msg.chat.type == 'channel'  # and message.chat_id == env['CHANNEL']
        has_eggplant = '🍆' in msg.text  # eggplant

        if msg.chat.id == env['GROUP']:
            if '🔔' in msg.text:  # bell
                self.__send_all_messages = True
            if '🔕' in msg.text:  # crossed out bell
                self.__send_all_messages = False

        return is_mention or is_reply or is_channel or has_eggplant or is_channel or self.__send_all_messages


halansky_filter = Filters.text & (InteractionWithBot() | Filters.private)
