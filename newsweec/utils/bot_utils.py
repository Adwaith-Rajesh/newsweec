# all the meta funcs related to the bot

from telebot.types import Message

from ._dataclasses import MessageInfo


def message_info_generator(msg: Message):
    """Get important info from the message
    like:
        chat_id, message_id, user_id, msg_text
    """
    return MessageInfo(user_id=msg.from_user.id, chat_id=msg.chat.id,
                       message_id=msg.message_id, text=msg.text)
