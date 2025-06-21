from flask import Flask, request, jsonify
import logging
from dingtalk_bot import DingTalkBot
from config import DINGTALK_ACCESS_TOKEN, SERVER_PORT, DINGTALK_KEYWORDS, DINGTALK_SECRET

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("server.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
ding_bot = DingTalkBot(
    access_token=DINGTALK_ACCESS_TOKEN,
    secret=DINGTALK_SECRET,
    keywords=DINGTALK_KEYWORDS
)


@app.route('/api/report', methods=['POST'])
def receive_report():
    try:
        data = request.json
        logger.info(f"Received report data: {data}")

        # 验证必要字段
        required_fields = ['program_name', 'status', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        program_name = data['program_name']
        status = data['status']
        message = data['message']
        details = data.get('details', {})

        # 获取并记录@人参数
        at_mobiles = data.get('at_mobiles', [])
        at_all = data.get('at_all', False)

        # 清理并验证手机号格式
        if at_mobiles:
            # 确保是字符串列表
            at_mobiles = [str(mobile).strip() for mobile in at_mobiles if mobile]
            logger.info(f"Will attempt to @ these mobiles: {at_mobiles}")

        # 构建通知消息
        title = f"程序运行通知: {program_name}"
        content = f"状态: {'成功' if status == 'success' else '失败'}\n"
        content += f"消息: {message}\n"

        if details:
            content += "\n详细信息:\n"
            for key, value in details.items():
                content += f"- {key}: {value}\n"

        # 添加显式的@标记
        if at_mobiles:
            for mobile in at_mobiles:
                content += f"\n@{mobile}"

        # 发送钉钉通知，明确传入@人参数
        success, response = ding_bot.send_markdown(
            title,
            content,
            at_mobiles=at_mobiles,
            at_all=at_all
        )

        logger.info(f"DingTalk notification result: {success}, response: {response}")
        return jsonify({"success": True, "ding_result": success}), 200

    except Exception as e:
        logger.error(f"Error processing report: {str(e)}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    logger.info(f"Starting server on port {SERVER_PORT}")
    app.run(host='0.0.0.0', port=SERVER_PORT)
