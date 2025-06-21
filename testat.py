#!/usr/bin/env python3
# 钉钉@人功能测试脚本

import sys
import logging
from dingtalk_bot import DingTalkBot
from config import DINGTALK_ACCESS_TOKEN, DINGTALK_SECRET, DINGTALK_KEYWORDS

# 设置日志
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_at_person():
    """测试@人功能"""
    # 创建机器人实例
    bot = DingTalkBot(
        access_token=DINGTALK_ACCESS_TOKEN,
        secret=DINGTALK_SECRET,
        keywords=DINGTALK_KEYWORDS
    )

    # 要@的手机号 - 替换为真实手机号
    mobile = input("请输入要@的手机号: ").strip()

    if not mobile:
        print("错误：未提供手机号")
        return

    # 1. 测试文本消息@人
    print("\n测试文本消息@人...")
    text_content = f"测试@人功能 这是一条测试消息"
    success, result = bot.send_text(text_content, at_mobiles=[mobile])
    print(f"文本@结果: {'成功' if success else '失败'}")
    print(f"API响应: {result}")

    # 2. 测试Markdown消息@人
    print("\n测试Markdown消息@人...")
    md_title = "测试@功能"
    md_content = f"""## 测试Markdown中@人

这是一条**Markdown**测试消息

### 重要提示
请注意查收这条消息 @{mobile}
    """

    success, result = bot.send_markdown(md_title, md_content, at_mobiles=[mobile])
    print(f"Markdown@结果: {'成功' if success else '失败'}")
    print(f"API响应: {result}")


if __name__ == "__main__":
    test_at_person()
