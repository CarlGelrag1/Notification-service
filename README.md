# Notification-Service

这是一个基于 Python 的钉钉通知服务模块，用于通过调用钉钉机器人接口实现消息推送功能，适用于企业内部的通知需求。

---

## 📌 项目功能
- 提供钉钉消息推送服务。
- 支持文本与 Markdown 格式的消息发送。
- 支持@指定人员或全体成员功能。
- 可通过 REST API 接口接收外部请求并发送通知。

---

## 🧩 目录结构
├── README.md # 项目说明文件 

├── app.py # Flask 主程序入口，提供 Web API 接收通知请求 

├── config.py # 配置文件，包含钉钉 Token 和服务器端口等信息 

├── dingtalk_bot.py # 钉钉机器人核心逻辑封装类 

├── testat.py # 测试脚本，用于测试 @人 功能 

---

## ⚙️ 技术栈
- **语言**: Python 3.x
- **框架**: Flask (用于构建 Web 服务)
- **第三方集成**: 钉钉机器人 API
- **依赖库**: requests, flask, hmac, hashlib 等

---

## 📦 运行服务

启动主服务：
python app.py
服务将在 `http://0.0.0.0:6020` 上运行，可以通过 `/api/report` 接口发送 POST 请求来触发通知。

---

## 📝 示例 API 请求体
json { 
    "program_name": "数据处理任务", 
    "status": "success", 
    "message": "任务执行完成", 
    "details": { 
        "records_processed": 100, 
        "duration_seconds": 5 
        }, 
    "at_mobiles": ["13800138000"], 
    "at_all": false 
    }
    ---

## 🧪 功能测试

你可以使用 `testat.py` 脚本来测试钉钉机器人的 `@人` 功能：
python testat.py
按照提示输入手机号即可进行测试。

---

## 💡 注意事项
- 替换 `config.py` 中的 `DINGTALK_ACCESS_TOKEN` 和 `DINGTALK_SECRET` 为自己的钉钉机器人密钥。
- 如果需要设置关键词过滤，请修改 `DINGTALK_KEYWORDS`。
- 服务默认监听端口为 `6020`，如需更改请在 `config.py` 中调整。

---
版权信息
本工具仅供学习和研究使用，请勿用于非法用途。使用本工具请遵循相关法律法规。
