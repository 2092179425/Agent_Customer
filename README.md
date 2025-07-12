# Agent_Customer 项目文档

## 项目概述
本项目名为 `Agent_Customer`，是一个集前端与后端于一体的综合性项目。前端采用 Vue 3 和 Vite 构建，为用户提供直观友好的交互界面；后端使用 Python 开发，处理业务逻辑和数据交互。

## 项目结构
```
Agent_Customer/
├── backend/
│   └── main.py           # 后端主程序，定义数据模型
├── frontend/
│   ├── public/
│   │   └── index.html    # 前端入口 HTML 文件
│   ├── src/
│   │   ├── App.vue       # 前端主 Vue 组件
│   │   ├── main.js       # 前端入口 JavaScript 文件
│   │   └── style.css     # 前端样式文件
│   ├── package.json      # 前端项目依赖配置
│   └── package-lock.json # 前端项目依赖锁定文件
└── .idea/                # IDE 配置文件
```

## 后端部分

### 数据模型
在 `backend/main.py` 文件中定义了 `ChatRequest` 数据模型，用于处理聊天请求：
```python
# 数据模型定义
class ChatRequest(BaseModel):
    user_id: str
    content: str
```

### 运行环境
项目后端依赖 Python 3.11 环境，可在 `.idea/misc.xml` 文件中查看配置：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="Black">
    <option name="sdkName" value="Python 3.11 (pycharm_test) (3)" />
  </component>
  <component name="ProjectRootManager" version="2" project-jdk-name="Python 3.11 (pycharm_test) (3)" project-jdk-type="Python SDK" />
</project>
```

### 运行步骤
1. 进入后端项目目录：
```bash
cd Agent_Customer/backend
```
2. 安装依赖（假设使用了虚拟环境）：
```bash
pip install -r requirements.txt  # 如果有 requirements.txt 文件
```
3. 启动后端服务（假设使用 uvicorn 运行 FastAPI 项目）：
```bash
uvicorn main:app --reload
```

## 前端部分

### 技术栈
- **Vue 3**：采用 `<script setup>` 语法糖，提升开发效率和代码可读性。
- **Vite**：快速的构建工具，支持热更新和高效打包。

### 依赖信息
前端项目依赖众多 npm 包，部分重要依赖及版本信息如下：
- **esbuild**：`^0.25.0`，多个平台相关版本要求 `node >= 18`。
- **rollup**：`^4.40.0`，版本为 `4.44.2`，要求 `node >= 18.0.0`，`npm >= 8.0.0`。
- **vite**：`7.0.2`，要求 `node ^20.19.0 || >=22.12.0`。

### 运行步骤
1. 进入前端项目目录：
```bash
cd Agent_Customer/frontend
```
2. 安装依赖：
```bash
npm install
```
3. 启动开发服务器：
```bash
npm run dev
```
4. 打开浏览器，访问 `http://localhost:5173` 查看前端界面。

### 构建项目
```bash
npm run build
```
构建后的文件将生成在 `dist` 目录下。

## 注意事项
- 前端项目部分依赖要求 `node >= 18`，请确保本地 Node.js 版本符合要求。
- 后端项目依赖 Python 3.11 环境，请确保 Python 版本正确。
