from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from datetime import datetime, timedelta
import random

class Send_to_MP:
    def __init__(self,app_id,app_secret,user_id,template_id):
        self._app_id =app_id
        self._app_secret=app_secret
        self._user_id=user_id
        self._template_id=template_id

    def _get_random_color(self):
        return "#%06x" % random.randint(0, 0xFFFFFF)

    def _send_to_mp(self, msg: str):
        tday = datetime.now() + timedelta(hours=8)
        tday = tday.strftime("%Y-%m-%d %H:%M:%S")
        client = WeChatClient(self._app_id, self._app_secret)
        wm = WeChatMessage(client)
        data = {
            "date": {"value": format(tday), "color": self._get_random_color()},
            "re": {"value": msg, "color": self._get_random_color()},
        }
        res = wm.send_template(self._user_id, self._template_id, data)