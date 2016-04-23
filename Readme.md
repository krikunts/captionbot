captionbot
--------

Captionbot is a simple API wrapper for https://captionbot.ai

To use, simply do:

    >>> from captionbot import CaptionBot
    >>> c = CaptionBot()
    >>> c.url_caption('your image url here')
    >>> c.file_caption('your local image filename here')