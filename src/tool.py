import os

from officy import JsonFile
from rumpy import FullNode

from config_rss import *


def init_group():
    bot = FullNode(port=RUM_PORT)
    if not os.path.exists(SEEDFILE):
        seed = bot.api.create_group("HELLO")
        JsonFile(SEEDFILE).write(seed)
    else:
        info = bot.api.group_info(group_id=RUM_GROUPID).__dict__
        print(info)
    print(SEEDFILE)


if __name__ == "__main__":
    init_group()
