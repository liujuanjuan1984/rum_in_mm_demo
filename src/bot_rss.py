import datetime
import json
import logging
import os
import re
import sys
import time

from config_rss import *
from modules import *

sys.path.insert(0, RUMPY_PATH)
import rumpy
from eth_account import Account
from eth_utils.hexadecimal import encode_hex
from rumpy import HttpRequest

logger = logging.getLogger(__name__)


class RssBot:
    def __init__(self, db_name=None):
        self.http = HttpRequest(api_base=RUM_HOST, jwt_token=RUM_JWT_TOKEN)
        self.db = BaseDB(db_name or DB_NAME, echo=False, reset=False)

    def get_pvtkey(self, mixin_id: str) -> str:
        key = self.db.session.query(KeyStore).filter(KeyStore.mixin_id == mixin_id).first()

        if key:
            keystore = json.loads(key.keystore)
            pvtkey = Account.decrypt(keystore, COMMON_ACCOUNT_PWD)
        else:
            account = Account.create()
            keystore = account.encrypt(COMMON_ACCOUNT_PWD)
            _k = {
                "mixin_id": mixin_id,
                "keystore": json.dumps(keystore),
            }

            self.db.add(KeyStore(_k))
            pvtkey = account.key
        return encode_hex(pvtkey)

    def rum_encrypt_data(self, content: str, pvtkey: str) -> str:
        if not content:
            return

        cmd = """node {0} {1} "{2}" {3} {4}""".format(RUM_LIGHT_JS_PATH, RUM_GROUPID, content, pvtkey, RUM_CIPHERKEY)
        nodejs = os.popen(cmd)
        m = nodejs.read()
        nodejs.close()
        rlts = re.findall(r"""TrxItem: ['"](.*?)['"]\n""", m)
        if rlts:
            return rlts[0]

        logger.warning(f"rum_encrypt_data content {content}")
        logger.warning(f"rum_encrypt_data m {m}")

    def send_to_rum(self):
        logger.info("send_to_rum start ...")
        data = self.db.session.query(BotComments).all()
        for r in data:
            if r.is_to_rum:
                continue
            if not r.text:
                continue

            pvtkey = self.get_pvtkey(r.user_id)
            logger.warning(f"内容 {r.text}")
            encryped_data = self.rum_encrypt_data(r.text, pvtkey)
            if not encryped_data:
                logger.warning(f"rum_encrypt_data 没成功？？{encryped_data}")
                continue

            resp = self.http.post(f"/api/v1/node/trx/{RUM_GROUPID}", {"TrxItem": encryped_data})

            logger.info(f"rum.api.send_note, message_id: {r.message_id}...")

            if "trx_id" not in resp:
                logger.warning(f"rum.api.send_note, resp: {json.dumps(resp)}")
                continue

            self.db.session.query(BotComments).filter(BotComments.message_id == r.message_id).update(
                {"is_to_rum": True}
            )
            self.db.commit()
            logger.info(f"rum.api.send_note, success. message_id: {r.message_id}...")

        logger.info("send_to_rum done")


if __name__ == "__main__":
    bot = RssBot()
    print(datetime.datetime.now(), "rss start...")
    while True:
        # try:
        bot.send_to_rum()
        # except Exception as e:
        #    print(e)
        time.sleep(1)
