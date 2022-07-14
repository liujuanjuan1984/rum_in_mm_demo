import datetime
import json
import logging
import re
import sys
import time

from config_rss import *

sys.path.insert(0, MIXIN_SDK_PATH)
from mixinsdk.clients.blaze_client import BlazeClient
from mixinsdk.clients.http_client import HttpClient_AppAuth
from mixinsdk.clients.user_config import AppConfig
from mixinsdk.types.message import MessageView, pack_message, pack_text_data

from modules import *

now = datetime.datetime.now()

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
    filename=f"rss_blaze_{datetime.date.today()}_{now.hour}_{now.minute}.log",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


class BlazeBot:
    def __init__(self, db_name=None):
        self.config = AppConfig.from_file(MIXIN_KEYSTORE_FILE)
        self.db = BaseDB(db_name or DB_NAME, echo=False, reset=False)

    def check_str_param(self, text):
        if type(text) == str:
            return text
        if type(text) == dict:
            return json.dumps(text)
        return str(text)

    def to_send_to_rum(self, msgview, db_session):
        _c = {
            "message_id": msgview.message_id,
            "is_reply": False,
            "is_to_rum": None,
            "quote_message_id": msgview.quote_message_id,
            "conversation_id": msgview.conversation_id,
            "user_id": msgview.user_id,
            "text": self.check_str_param(msgview.data_decoded),
            "category": msgview.category,
            "timestamp": str(msgview.created_at),
        }

        db_session.add(BotComments(_c))
        is_to_rum = len(msgview.data_decoded) > 10
        if is_to_rum:
            db_session.query(BotComments).filter(BotComments.message_id == msgview.message_id).update(
                {"is_reply": True, "is_to_rum": False}
            )
            db_session.commit()
        logger.debug(f"need to_send_to_rum? {is_to_rum}, message_id: {msgview.message_id}")
        return is_to_rum

    def get_reply_text(self, text):
        return WELCOME_TEXT


def message_handle_error_callback(error, details):
    logger.error("===== error_callback =====")
    logger.error(f"error: {error}")
    logger.error(f"details: {details}")


async def message_handle(message):
    global bot
    db_session = bot.db.Session()
    action = message["action"]

    if action == "ACKNOWLEDGE_MESSAGE_RECEIPT":
        # logger.info("Mixin blaze server: received the message")
        return

    if action == "LIST_PENDING_MESSAGES":
        # logger.info("Mixin blaze server: list pending message")
        return

    if action == "ERROR":
        logger.warning(message["error"])
        await bot.blaze.echo(msgview.message_id)
        return

    if action != "CREATE_MESSAGE":
        await bot.blaze.echo(msgview.message_id)
        return

    error = message.get("error")
    if error:
        logger.info(str(error))
        await bot.blaze.echo(msgview.message_id)
        return

    msgview = MessageView.from_dict(message["data"])

    # 和 server 有 -8 时差。也就是只处理 1 小时内的 message
    if msgview.created_at <= datetime.datetime.now() + datetime.timedelta(hours=-9):
        await bot.blaze.echo(msgview.message_id)
        return

    if msgview.type != "message":
        await bot.blaze.echo(msgview.message_id)
        return

    if msgview.conversation_id in ("", None):
        await bot.blaze.echo(msgview.message_id)
        return

    if msgview.data_decoded in ("", None):
        await bot.blaze.echo(msgview.message_id)
        return

    if type(msgview.data_decoded) != str:
        await bot.blaze.echo(msgview.message_id)
        return
    # record the message
    # 查询 bot_comments

    logger.info(
        f"msgview {str(msgview.created_at+datetime.timedelta(hours=8))}, user_id: {msgview.user_id}, message_id {msgview.message_id}"
    )

    existed = db_session.query(BotComments).filter(BotComments.message_id == msgview.message_id).first()
    # 消息没有计入数据库，就写入
    reply_text = ""
    if existed == None:
        logger.debug(f"not existed in db. message_id {msgview.message_id}")
        if bot.to_send_to_rum(msgview, db_session=db_session):
            await bot.blaze.echo(msgview.message_id)
            reply_text = "收到，数据自动上链中"

    # 已经响应过的，就不再回复
    else:
        logger.debug(f"existed in db. message_id {msgview.message_id}. is_reply:{existed.is_reply}")
        if existed.is_reply == True:
            await bot.blaze.echo(msgview.message_id)
            return
    if not reply_text:
        reply_text = bot.get_reply_text(msgview.data_decoded)
    # send reply

    msg = pack_message(
        pack_text_data(reply_text),
        conversation_id=msgview.conversation_id,
        quote_message_id=msgview.message_id,
    )
    logger.debug(f"pack_message {msgview.message_id} {reply_text}")
    resp = bot.xin.api.send_messages(msg)
    logger.debug(f"pack_message resp??? {json.dumps(resp)}")

    if "data" in resp:
        logger.info(f"bot.xin.api.send_messages success. message_id: {msgview.message_id}")
        await bot.blaze.echo(msgview.message_id)
        db_session.query(BotComments).filter(BotComments.message_id == msgview.message_id).update({"is_reply": True})
        db_session.commit()
        logger.info(f"bot.xin.api.send_messages success to db. message_id: {msgview.message_id}")
    else:
        logger.info(f"xin.api.send_messages {json.dumps(resp)}")
    return


bot = BlazeBot()
bot.xin = HttpClient_AppAuth(bot.config)
bot.blaze = BlazeClient(
    bot.config,
    on_message=message_handle,
    on_message_error_callback=message_handle_error_callback,
)


bot.blaze.run_forever(2)
