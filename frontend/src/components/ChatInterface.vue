<template>
  <div class="chat-container">
    <!-- 聊天头部 -->
    <div class="chat-header">
      <div class="avatar">
        <img src="../assets/aislogo.svg" alt="客服头像" width="40" height="40">
      </div>
      <h2>智能客服</h2>
    </div>

    <!-- 聊天内容区域 -->
    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message"
        :class="msg.isUser ? 'user-message' : 'bot-message'"
      >
        <div class="message-avatar">
          <img v-if="msg.isUser" src="../assets/user.svg" alt="用户头像" width="30" height="30">
          <img v-else src="../assets/aislogo.svg" alt="客服头像" width="30" height="30">
        </div>
        <div class="message-content">{{ msg.text }}</div>
      </div>

      <!-- 加载中指示器 -->
      <div v-if="isLoading" class="message bot-message">
        <div class="message-avatar">
          <img src="../assets/aislogo.svg" alt="客服头像" width="30" height="30">
        </div>
        <div class="typing-indicator">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input">
      <input
        v-model="userInput"
        type="text"
        placeholder="请输入您的问题..."
        @keydown.enter="sendMessage"
      >
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

// 状态管理
const userInput = ref('');
const messages = ref([]);
const isLoading = ref(false);
const messagesContainer = ref(null);
const userId = ref('');

// 生成随机用户ID
const generateUserId = () => {
  return 'user_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
};

// 初始化用户ID
onMounted(() => {
  // 从localStorage获取用户ID，不存在则生成新的
  const storedUserId = localStorage.getItem('kouz智能客服_userId');
  if (storedUserId) {
    userId.value = storedUserId;
  } else {
    const newUserId = generateUserId();
    userId.value = newUserId;
    localStorage.setItem('kouz智能客服_userId', newUserId);
  }

  // 添加欢迎消息
  if (messages.value.length === 0) {
    messages.value.push({
      text: '您好！我是智能客服，请问有什么可以帮助您的吗？',
      isUser: false
    });
  }

  // 自动滚动到底部
  scrollToBottom();
});

// 监听消息变化，自动滚动到底部
watch(messages, () => {
  scrollToBottom();
});

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 发送消息
const sendMessage = () => {
  if (!userInput.value.trim()) return;

  // 添加用户消息
  messages.value.push({
    text: userInput.value.trim(),
    isUser: true
  });

  // 清空输入框
  const inputText = userInput.value.trim();
  userInput.value = '';

  // 调用后端接口获取回复
  getBotResponse(inputText);
};

// 调用后端接口获取流式响应
const getBotResponse = async (message) => {
  isLoading.value = true;

  try {
    // 创建一个临时消息用于展示流式响应
    const botMessageIndex = messages.value.length;
    messages.value.push({ text: '', isUser: false });

    // 调用后端流式接口
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId.value, content: message })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      // 将增量内容添加到对话界面
      messages.value[botMessageIndex].text += chunk;
    }
  } catch (error) {
    console.error('获取回复失败:', error);
    messages.value[messages.value.length - 1].text = '抱歉，获取回复失败，请稍后再试。';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  width: 90%;
  max-width: 2000px; 
  height: 95vh;
  margin: 20px auto;
  border: 1px solid #e8e8e8;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  background-color: #f9f9f9;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

@media (min-width: 1600px) {
  .chat-container {
    width: 70%;
    max-width: 1800px;
  }
}

@media (max-width: 768px) {
  .chat-container {
    width: 100%;
    height: calc(100vh - 50px); 
    margin: 0 auto;
    border-radius: 8px; 
  }
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 18px 24px;
  background: linear-gradient(135deg, #00d9fa 0%, #a9ecf7 100%);
  color: white;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.8);
  position: relative;
  z-index: 10;
}

.chat-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.chat-header h2 {
  margin: 0;
  font-size: 2.0rem;
  font-weight: 900;
  letter-spacing: 0.3px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.avatar {
  margin-right: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  padding: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: contain;
}

.chat-messages {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #f5f9fa;
  background-image: linear-gradient(#ffffff 1px, transparent 1px),
                    linear-gradient(90deg, #fff 1px, #f5f7fa 1px);
  background-size: 20px 20px;
}

.message {
  display: flex;
  margin-bottom: 16px;
  max-width: 70%;
  transition: transform 0.2s ease;
}

.message:hover {
  transform: translateY(-1px);
}

.user-message {
  flex-direction: row-reverse;
  margin-left: auto;
}

.message-avatar {
  margin-right: 12px;
  margin-left: 12px;
}

.message-avatar img {
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.message-content {
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.5;
  font-size: 0.95rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  word-break: break-word;
}

.user-message .message-content {
  background: linear-gradient(135deg, #34a853 0%, #2d924b 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.bot-message .message-content {
  background-color: white;
  color: #2d3748;
  border: 1px solid #e8e8e8;
  border-bottom-left-radius: 4px;
}

.chat-input {
  display: flex;
  padding: 16px;
  border-top: 1px solid #38a5f4;
  background-color: rgb(186, 225, 232);
}

.chat-input input {
  flex: 1;
  padding: 12px 18px;
  border: 1px solid #e0e0e0;
  border-radius: 24px;
  outline: none;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background-color: #f8f9fa;
  color: #333;
}

.chat-input input:focus {
  border-color: #3da7cd;
  box-shadow: 0 0 0 2px rgba(61, 167, 205, 0.2);
}

.chat-input button {
  margin-left: 12px;
  padding: 12px 24px;
  background: linear-gradient(135deg, #00d9fa 0%, #a9ecf7 200%);
  color: white;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.chat-input button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: white;
  border-radius: 18px;
  border: 1px solid #e8e8e8;
}

.dot {
  width: 8px;
  height: 8px;
  margin: 0 4px;
  background-color: #a0aec0;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.6; }
  30% { transform: translateY(-4px); opacity: 1; }
}

/* 自定义滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>