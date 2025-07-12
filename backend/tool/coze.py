from cozepy import COZE_CN_BASE_URL, Coze, TokenAuth, Message, ChatEventType
import os
from typing import Dict, Optional, Generator

class CozeAPI:
    """Coze API调用封装类"""

    def __init__(self, api_token: str = None, bot_id: str = None):
        """
        初始化Coze API客户端

        Args:
            api_token (str): Coze API Token，默认为环境变量中的值
            bot_id (str): 机器人ID，默认为环境变量中的值
        """
        self.api_token = api_token or os.getenv("COZE_API_TOKEN")
        self.bot_id = bot_id or os.getenv("BOT_ID")

        if not self.api_token or not self.bot_id:
            raise ValueError("Coze API Token和Bot ID是必需的")

        self.client = Coze(
            auth=TokenAuth(token=self.api_token),
            base_url=COZE_CN_BASE_URL
        )

    def stream_chat(self, user_id: str, content: str) -> Generator[str, None, None]:
        """
        流式对话接口

        Args:
            user_id (str): 用户ID
            content (str): 用户输入内容

        Yields:
            str: 对话的增量内容
        """
        try:
            for event in self.client.chat.stream(
                    bot_id=self.bot_id,
                    user_id=user_id,
                    conversation_id='7524681701780602880',
                    additional_messages=[
                        Message.build_user_question_text(content),
                    ]
            ):
                if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
                    if event.message.content:
                        yield event.message.content

                elif event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
                    # 可以在这里添加结束标记或其他元数据
                    break

        except Exception as e:
            # 生成错误信息
            yield f"错误: {str(e)}"

    def complete_chat(self, user_id: str, content: str) -> Dict:
        """
        完整对话接口（非流式）

        Args:
            user_id (str): 用户ID
            content (str): 用户输入内容

        Returns:
            Dict: 包含回复文本和token使用量的字典
        """
        result = {
            "response_text": "",
            "token_usage": 0,
            "error": None
        }

        try:
            for event in self.stream_chat(user_id, content):
                if event.startswith("错误: "):
                    result["error"] = event[4:]  # 去掉"错误: "前缀
                    break
                result["response_text"] += event

            # 如果没有错误，设置token使用量（需要从Coze API获取）
            # 注意：当前cozepy库的流式API在完成事件中返回token使用量
            # 这里简化处理，实际项目中可能需要调整

        except Exception as e:
            result["error"] = str(e)

        return result