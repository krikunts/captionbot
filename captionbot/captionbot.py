import json
import mimetypes
import os
import requests
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import logging
logger = logging.getLogger("captionbot")


class CaptionBotException(Exception):
    pass


class CaptionBot:
    BASE_URL = "https://www.captionbot.ai/api/"

    @staticmethod
    def _resp_error(resp):
        if not resp.ok:
            data = resp.json()
            msg = "HTTP error: {}".format(resp.status_code)
            if type(data) == dict and "Message" in data:
                msg += ", " + data.get("Message")
            raise CaptionBotException(msg)

    def __init__(self):
        self.session = requests.Session()
        url = self.BASE_URL + "init"
        resp = self.session.get(url, verify=False)
        logger.debug("init: {}".format(resp))
        self._resp_error(resp)
        self.conversation_id = resp.json()
        self.watermark = ''

    def _upload(self, filename):
        url = self.BASE_URL + "upload"
        mime = mimetypes.guess_type(filename)[0]
        name = os.path.basename(filename)
        files = {'file': (name, open(filename, 'rb'), mime)}
        resp = self.session.post(url, files=files, verify=False)
        logger.debug("upload: {}".format(resp))
        self._resp_error(resp)
        return resp.json()

    def url_caption(self, image_url):
        data = {
            "userMessage": image_url,
            "conversationId": self.conversation_id,
            "waterMark": self.watermark
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        url = self.BASE_URL + "message"
        resp = self.session.post(url, data=json.dumps(data), headers=headers, verify=False)
        logger.info("get_caption: {}".format(resp))
        if not resp.ok:
            return None
        get_url = url + "?" + urlencode(data)
        resp = self.session.get(get_url, verify=False)
        if not resp.ok:
            return None
        text = resp.text[1:-1].replace('\\"', '"')
        res = json.loads(text)
        logger.info(res)
        self.watermark = res.get("WaterMark")
        msg = res.get("BotMessages")[1].replace('\\n','\n')
        return msg

    def file_caption(self, filename):
        upload_filename = self._upload(filename)
        return self.url_caption(upload_filename)