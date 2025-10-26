# 快速开始指南

## 5分钟快速开始

### 步骤1：安装环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 步骤2：配置API密钥

```bash
# 复制配置文件
cp .env.example .env

# 编辑.env文件，添加你的OpenAI API Key
# 你可以从 https://platform.openai.com/api-keys 获取
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 步骤3：运行示例

```bash
python rag_demo.py
```

就是这么简单！🎉

## 预期输出

第一次运行时会看到：
1. 组件初始化
2. 加载文档
3. 文档分割
4. 向量化
5. 创建问答链
6. 运行测试查询

## 下一步

1. 添加你自己的文档到 `documents/` 目录
2. 运行 `python example_usage.py` 进行交互式查询
3. 阅读 `README.md` 了解高级用法
4. 查看源代码 `rag_demo.py` 学习实现细节

## 常见问题

**Q: 我遇到 "OPENAI_API_KEY not found" 错误**
A: 确保你在 `.env` 文件中设置了API密钥，并正确激活了虚拟环境。

**Q: 没有Python包可用**
A: 确保已安装依赖：`pip install -r requirements.txt`

**Q: 想添加自己的文档**
A: 将PDF或TXT文件放入 `documents/` 目录即可。

## 需要帮助？

查看完整的 `README.md` 了解更多细节。
