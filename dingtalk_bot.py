# dingtalk_bot.py
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import logging

logger = logging.getLogger(__name__)


class DingTalkBot:
    def __init__(self, access_token, secret=None, keywords=None):
        """
        初始化钉钉机器人客户端
        参数:
            access_token: 钉钉机器人的access_token
            secret: 钉钉机器人的加签密钥（SEC开头的字符串）
            keywords: 自定义关键词列表，消息必须包含其中之一
        """
        self.access_token = access_token
        self.secret = secret
        self.keywords = keywords or []
        self.url = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}"

    def _get_signed_url(self):
        """生成带签名的URL"""
        if not self.secret:
            return self.url

        timestamp = str(round(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            self.secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return f"{self.url}&timestamp={timestamp}&sign={sign}"

    def _ensure_keyword_exists(self, text):
        """确保文本中包含至少一个关键词"""
        if not self.keywords:
            return text  # 没有设置关键词要求，直接返回原文本

        # 检查文本是否已经包含关键词
        for keyword in self.keywords:
            if keyword in text:
                return text

        # 如果不包含任何关键词，添加第一个关键词到开头
        return f"{self.keywords[0]} {text}"

    def send_text(self, content, at_mobiles=None, at_all=False):
        """
        发送文本消息
        参数:
            content: 消息内容
            at_mobiles: 需要@的手机号列表
            at_all: 是否@所有人
        """
        url = self._get_signed_url()
        content = self._ensure_keyword_exists(content)

        # 在文本中添加@手机号标记，按照钉钉要求格式
        if at_mobiles and at_mobiles[0]:
            at_text = ""
            for mobile in at_mobiles:
                if mobile:  # 确保手机号非空
                    at_text += f" @{mobile}"
            content += at_text

        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }

        return self._send_request(url, data)

    def send_markdown(self, title, text, at_mobiles=None, at_all=False):
        """
        发送markdown消息
        参数:
            title: 消息标题
            text: markdown格式的消息内容
            at_mobiles: 需要@的手机号列表
            at_all: 是否@所有人
        """
        url = self._get_signed_url()
        text = self._ensure_keyword_exists(text)

        # 根据钉钉文档要求，在markdown文本中添加@手机号标记
        # if at_mobiles and at_mobiles[0]:  # 确保有有效的手机号
        #     # 在markdown文本末尾添加@标记
        #     text += "\n\n"  # 添加空行
        #     for mobile in at_mobiles:
        #         if mobile:  # 确保手机号非空
        #             text += f"@{mobile} "

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": at_all
            }
        }

        # 记录完整的请求数据便于调试
        logger.info(f"Sending markdown with at.atMobiles: {at_mobiles}")

        return self._send_request(url, data)

    def _send_request(self, url, data):
        """发送请求到钉钉API"""
        try:
            # 记录完整请求内容
            logger.info(f"Sending request to DingTalk API: {url}")
            logger.info(f"Request data: {data}")

            response = requests.post(url, json=data)
            result = response.json()

            if result.get('errcode') == 0:
                logger.info(f"Message sent successfully: {result}")
                return True, result
            else:
                logger.error(f"Failed to send message: {result}")
                return False, result

        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False, {"error": str(e)}
