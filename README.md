# RAG + LangChain + Ollama 本地模型演示

一个基于检索增强生成（RAG）技术的本地知识库问答系统，使用 Ollama 本地大语言模型和 FAISS 向量数据库。

## ✨ 特性

- 🏠 **完全本地运行** - 使用 Ollama 本地模型，无需API密钥
- 📚 **多文档支持** - 支持 PDF 和 TXT 格式文档
- 🔍 **智能检索** - 使用 FAISS 向量数据库进行语义检索
- 🎯 **细粒度文档分割** - 300字符分块，提高检索精度
- 💬 **完整RAG流程** - 文档加载、向量化、检索、生成一体化
- 📊 **来源追踪** - 返回答案的同时提供来源文档

## 🏗️ 技术栈

- **Python 3.14+**
- **LangChain** - LLM应用框架
- **Ollama** - 本地LLM和Embedding模型
- **FAISS** - Facebook相似性搜索库
- **模型**:
  - Embedding: `nomic-embed-text`
  - LLM: `llama3:8b`

## 📁 项目结构

```
rag_langchain_demo/
├── rag_demo.py          # 主程序
├── requirements.txt     # 依赖包
├── README.md           # 项目说明
├── .env.example        # 环境变量示例
├── .gitignore          # Git忽略规则
├── documents/          # 文档目录
│   ├── sample_document.txt
│   └── advanced_topics.txt
└── vectorstore/        # 向量数据库（自动生成）
    ├── index.faiss
    └── index.pkl
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/Yhorm-LZ/rag_langchain_demo.git
cd rag_langchain_demo

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 安装Ollama模型

```bash
# 下载embedding模型
ollama pull nomic-embed-text

# 下载LLM模型
ollama pull llama3:8b
```

### 3. 准备文档

将要查询的文档（PDF或TXT格式）放入 `documents/` 目录。

### 4. 运行程序

```bash
python rag_demo.py
```

程序会自动：
- 加载并分割文档
- 生成向量嵌入
- 创建FAISS向量数据库
- 运行示例查询

## 💻 使用示例

### 基本使用

```python
from rag_demo import SimpleRAG

# 创建RAG实例
rag = SimpleRAG(
    documents_path="./documents",
    embedding_model="nomic-embed-text",
    llm_model="llama3:8b",
    use_ollama=True
)

# 初始化系统
rag.initialize_full_system()

# 查询
result = rag.query("RAG的工作原理是什么？")
print(result["answer"])
```

### 切换到OpenAI

```python
# 在 rag_demo.py 的 main() 函数中设置
use_ollama = False  # 使用OpenAI而不是Ollama

# 需要在 .env 文件中配置 OPENAI_API_KEY
```

### 自定义参数

```python
# 调整文档分块大小
split_docs = rag.split_documents(chunk_size=300, chunk_overlap=50)

# 调整检索数量
rag.create_qa_chain(k=4)
```

## ⚙️ 配置说明

### Ollama配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `embedding_model` | `nomic-embed-text` | 嵌入模型 |
| `llm_model` | `llama3:8b` | 对话模型 |
| `chunk_size` | 300 | 文档分块大小 |
| `chunk_overlap` | 50 | 分块重叠大小 |
| `k` | 4 | 检索相关文档数量 |

### OpenAI配置

```bash
# 在 .env 文件中设置
OPENAI_API_KEY=sk-your-api-key-here
```

## 🎯 工作流程

```
文档加载
    ↓
文档分割 (300字符/块)
    ↓
向量化 (nomic-embed-text)
    ↓
存储到FAISS
    ↓
用户查询
    ↓
检索相关文档
    ↓
LLM生成回答
    ↓
返回答案+来源
```

## 📊 示例输出

```
🎯 使用Ollama本地模型
   Embedding模型: nomic-embed-text
   LLM模型: llama3:8b
==================================================
开始初始化RAG系统
==================================================
正在初始化组件...
组件初始化完成！
正在从 ./documents 加载文档...
✓ 加载TXT: advanced_topics.txt
✓ 加载TXT: sample_document.txt
总共加载了 2 个文档片段
正在分割文档...
文档已分割为 12 个片段
向量存储已创建: ./vectorstore
向量存储中包含 12 个文档

问题: RAG的工作原理是什么？
--------------------------------------------------

回答: 根据上下文，RAG技术的工作原理包括：
1. 文档加载和预处理
2. 文档向量化
3. 问题向量化
4. 相似度检索
5. 上下文增强生成

来源文档:
  [1] ./documents/sample_document.txt
       ## RAG技术
       ...
```

## 🔧 故障排除

### 问题1: Ollama连接失败

```bash
# 检查Ollama服务
ollama list

# 重启Ollama
# macOS: 重启Ollama应用
# Linux: systemctl restart ollama
```

### 问题2: 模型未下载

```bash
# 下载所需模型
ollama pull nomic-embed-text
ollama pull llama3:8b
```

### 问题3: Python版本问题

项目需要 Python 3.14 或更高版本。如果遇到兼容性问题，可以使用 Python 3.10+。

### 问题4: 内存不足

如果处理大文档时内存不足，可以：
- 减小 `chunk_size`
- 使用更小的模型
- 减少 `k` 值（检索数量）

## 📚 学习要点

### RAG的核心概念

1. **检索（Retrieval）** - 根据问题找到最相关的文档片段
2. **增强（Augmented）** - 将检索到的上下文注入到提示中
3. **生成（Generation）** - 基于增强上下文生成回答

### 关键组件

- **RecursiveCharacterTextSplitter** - 递归字符分割器
- **FAISS** - 向量相似度搜索
- **OllamaEmbeddings** - 本地嵌入模型
- **ChatOllama** - 本地对话模型
- **RetrievalQA** - 检索增强问答链

### 最佳实践

- ✅ 文档分块大小：300-500字符（精准检索）
- ✅ 分块重叠：chunk_size的10-20%（保持上下文）
- ✅ 检索数量：k=3-5（平衡准确性和噪音）
- ✅ 温度参数：0.7（平衡创造性和准确性）

## 📦 依赖包

```
langchain>=0.3.0
langchain-community>=0.3.0
langchain-openai>=0.3.0
langchain-ollama>=0.1.0
langchain-classic>=1.0.0
python-dotenv>=1.0.0
pypdf>=4.0.0
openai>=2.0.0
faiss-cpu>=1.7.8
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**Happy Coding with RAG! 🚀**
