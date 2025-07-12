import os
import uuid
import asyncio
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator, Optional
from tool.coze import CozeAPI  # 导入Coze API封装类

# 初始化FastAPI应用
app = FastAPI(title="智能客服对话接口", description="基于Coze API的智能客服流式对话接口")

# 配置 - 建议生产环境使用环境变量存储敏感信息
COZE_API_TOKEN = os.getenv("COZE_API_TOKEN", "your token")
BOT_ID = os.getenv("BOT_ID", "your bot id")

# 数据模型定义
class ChatRequest(BaseModel):
    user_id: str
    content: str

class ChatResponse(BaseModel):
    response_text: str
    token_usage: int = 0
    error: Optional[str] = None

# 创建Coze API实例
coze_api = CozeAPI(api_token=COZE_API_TOKEN, bot_id=BOT_ID)

async def coze_stream_generator(user_id: str, content: str) -> AsyncGenerator[str, None]:
    """将Coze API的同步生成器转换为异步生成器"""
    for chunk in coze_api.stream_chat(user_id, content):
        yield chunk
        # 为了避免阻塞事件循环，添加微小延迟
        await asyncio.sleep(0)

@app.post("/api/chat/stream", response_class=StreamingResponse)
async def stream_chat(request: ChatRequest):
    """流式对话接口"""
    if not request.user_id or not request.content.strip():
        raise HTTPException(status_code=400, detail="用户ID和内容不能为空")

    return StreamingResponse(
        coze_stream_generator(request.user_id, request.content),
        media_type="text/event-stream"
    )

@app.post("/api/chat", response_model=ChatResponse)
def complete_chat(request: ChatRequest):
    """完整对话接口（非流式）"""
    if not request.user_id or not request.content.strip():
        raise HTTPException(status_code=400, detail="用户ID和内容不能为空")

    result = coze_api.complete_chat(request.user_id, request.content)
    return ChatResponse(**result)

@app.get("/api/health")
def health_check():
    """服务健康检查接口"""
    return {"status": "healthy", "service": "coze-chat-api"}

# 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True  # 开发环境使用，生产环境关闭
    )