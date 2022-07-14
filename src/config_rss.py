import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DB_NAME = f"sqlite:///rss_bot_test.db"

RUM_GROUPID = "27ab3bcd-3a32-4bff-9778-0d4a5c776925"

COMMON_ACCOUNT_PWD = RUM_GROUPID
# 从 seed 中解析得出
RUM_CIPHERKEY = "bca953e6b5062f3280cf447d4e821419d77497e55514c9b37ba1aace89fb4e2c"


RUM_HOST = "http://127.0.0.1:31194"

RUM_JWT_TOKEN = ""

WELCOME_TEXT = """👋 hello 正在开发中，欢迎围观 👨‍👩‍👧‍👦
轻直接对 bot 发送文本，bot 将自动为您绑定一个 Rum 账号，并把文本发送到 rum group 上👨‍👩‍👧‍👦"""
RUM_PORT = 31194  # FULL NODE TO CREATE GROUP

SEEDFILE = os.path.join(BASE_DIR, "seed.json")

CODE_DIR = os.path.dirname(BASE_DIR)
# git clone https://github.com/liujuanjuan1984/rumpy
RUMPY_PATH = os.path.join(CODE_DIR, "rumpy")
# git clone https://github.com/liujuanjuan1984/mixin-sdk-python
MIXIN_SDK_PATH = os.path.join(CODE_DIR, "mixin-sdk-python")

MIXIN_KEYSTORE_FILE = os.path.join(BASE_DIR, "mixin_bot_keystore.json")
RUM_LIGHT_JS_PATH = os.path.join(CODE_DIR, "quorum-light-node-sdk-to-py", "createTrxItemTwo.js")
