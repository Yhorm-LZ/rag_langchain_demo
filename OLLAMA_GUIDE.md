# Ollama 本地模型使用指南

## 📋 快速开始

### 1. 安装Ollama

访问 [https://ollama.ai](https://ollama.ai) 下载并安装Ollama。

### 2. 下载推荐模型

```bash
# 下载embedding模型
ollama pull nomic-embed-text

# 下载LLM对话模型
ollama pull llama3.2
```

### 3. 确保Ollama服务运行

```bash
# 检查Ollama是否运行
curl http://localhost:11434/api/tags

# 应该返回已安装的模型列表
```

### 4. 运行项目

```bash
cd /Users/yhorm/rag_langchain_demo
source .venv/bin/activate
python3 rag_demo.py
```

## 🔧 配置说明

### 在代码中切换模式

编辑 `rag_demo.py` 的 `main()` 函数：

```python
def main():
    # 使用Ollama
    use_ollama = True  # 设置为True使用Ollama
    
    if use_ollama:
        embedding_model = "nomic-embed-text"
        llm_model = "llama3.2"
    else:
        # 使用OpenAI
        embedding_model = "text-embedding-3-small"
        llm_model = "gpt-3.5-turbo"
```

### 修改Ollama配置

在 `rag_demo.py` 第31-44行，可以修改：

```python
self.llm = ChatOllama(
    model=self.llm_model,                    # 修改模型名称
    temperature=self.temperature,
    base_url="http://localhost:11434"        # 修改Ollama地址
)
```

## 📦 推荐模型

### Embedding模型（向量化）
- `nomic-embed-text` - 推荐，性能好
- `mxbai-embed-large` - 高质量
- `all-minilm` - 轻量级

### LLM对话模型
- `llama3.2` - 推荐，平衡性能和质量
- `llama3.2:3b` - 轻量级
- `mistral` - 快速响应
- `qwen2.5` - 中文优化

## 🔍 可用的Ollama模型

查看所有可用模型：
```bash
ollama list
```

搜索embedding模型：
```bash
ollama search embedding
```

搜索LLM模型：
```bash
ollama search llama
```

## ⚙️ 高级配置

### 修改向量维度

如果使用不同embedding模型，可能需要重新创建向量库：

```bash
# 删除旧向量库
rm -rf ./vectorstore

# 重新运行程序
python3 rag_demo.py
```

### 使用GPU加速

确保Ollama使用GPU：
```bash
# 检查GPU支持
ollama ps

# 下载支持GPU的模型
ollama pull llama3.2
```

## 🐛 常见问题

### Q: 连接Ollama失败
A: 确保Ollama服务正在运行
```bash
curl http://localhost:11434/api/tags
```

### Q: 模型不存在
A: 先下载模型
```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

### Q: 内存不足
A: 使用更小的模型
```python
llm_model = "llama3.2:1b"  # 1B参数版本
```

### Q: 速度太慢
A: 
1. 使用更小的模型
2. 确保使用GPU加速
3. 减少文档数量

## 📊 性能对比

| 特性 | Ollama本地 | OpenAI |
|------|-----------|--------|
| 成本 | 免费 | 付费 |
| 隐私 | 完全本地 | 云端 |
| 网络 | 不需要 | 需要 |
| 速度 | 取决于硬件 | 稳定快速 |
| 质量 | 取决于模型 | 高质量 |

## 🎯 下一步

1. 尝试不同的模型组合
2. 调整temperature参数
3. 优化文档分割策略
4. 探索高级LangChain功能

