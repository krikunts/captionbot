import json
import mimetypes
import os
import requests
import logging
logger = logging.getLogger("captionbot")


class CaptionBot:
    BASE_URL = "https://www.captionbot.ai/api/"

    def __init__(self):
        self.session = requests.Session()
        url = self.BASE_URL + "init"
        resp = self.session.get(url, verify=False)
        logger.debug("init: {}".format(resp))
        self.conversation_id = json.loads(resp.text)
        self.watermark = ''

    def _upload(self, filename):
        url = self.BASE_URL + "upload"
        mime = mimetypes.guess_type(filename)[0]
        name = os.path.basename(filename)
        files = {'file': (name, open(filename, 'rb'), mime)}
        resp = self.session.post(url, files=files, verify=False)
        logger.debug("upload: {}".format(resp))
        return json.loads(resp.text)

    def url_caption(self, image_url):
        data = json.dumps({
            "userMessage": image_url,
            "conversationId": self.conversation_id,
            "waterMark": self.watermark
        })
        headers = {
            "Content-Type": "application/json"
        }
        url = self.BASE_URL + "message"
        resp = self.session.post(url, data=data, headers=headers, verify=False)
        logger.debug("url_caption: {}".format(resp))
        if not resp.ok:
            return None
        res = json.loads(json.loads(resp.text))
        self.watermark = res.get("WaterMark")
        return res.get("UserMessage")

    def file_caption(self, filename):
        upload_filename = self._upload(filename)
        return self.url_caption(upload_filename)