# RAG + LangChain 演示项目

这是一个完整的RAG（Retrieval-Augmented Generation，检索增强生成）演示项目，展示了如何构建一个能够基于文档回答问题的AI系统，并与LangChain的LLM集成使用。

## 📚 项目简介

本项目实现了一个简单的RAG系统，包括：

1. **文档加载**：支持PDF和TXT格式的文档
2. **文档分割**：将长文档切分为适合处理的小片段
3. **向量化存储**：使用Chroma作为向量数据库
4. **语义检索**：根据问题检索相关文档片段
5. **增强生成**：使用LangChain的LLM基于检索到的上下文生成回答

## 🎯 核心功能

- ✅ 多格式文档加载（PDF、TXT）
- ✅ 自动文档分割和向量化
- ✅ 语义相似度检索
- ✅ 基于上下文的问答生成
- ✅ 引用来源文档
- ✅ 可配置的模型参数

## 🏗️ 技术栈

- **LangChain**：LLM应用框架
- **Chroma**：向量数据库
- **OpenAI Embeddings**：文本嵌入模型
- **OpenAI GPT**：大语言模型
- **Python 3.8+**

## 📁 项目结构

```
rag_langchain_demo/
├── rag_demo.py          # 主程序文件
├── example_usage.py     # 使用示例
├── requirements.txt     # 依赖包
├── .env.example         # 环境变量示例
├── README.md            # 项目说明
├── documents/           # 文档目录（放入您的PDF或TXT文件）
│   └── sample_document.txt  # 示例文档
└── vectorstore/         # 向量数据库存储（自动生成）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
# venv\Scripts\activate  # Windows

# 安装依赖包
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑.env文件，填入你的OpenAI API Key
# OPENAI_API_KEY=sk-your-api-key-here
```

### 3. 准备文档

将要查询的文档（PDF或TXT格式）放入 `documents/` 目录。项目已包含一个示例文档。

### 4. 运行程序

#### 方式一：直接运行主程序

```bash
python rag_demo.py
```

这将自动初始化系统并运行一些示例查询。

#### 方式二：交互式查询

```bash
python example_usage.py
```

这将启动一个交互式会话，你可以输入自己的问题。

### 5. 自定义使用

```python
from rag_demo import SimpleRAG

# 创建RAG实例
rag = SimpleRAG(
    documents_path="./documents",
    embedding_model="text-embedding-3-small",
    llm_model="gpt-3.5-turbo",
    temperature=0.7
)

# 初始化系统
rag.initialize_full_system()

# 查询问题
result = rag.query("人工智能的主要技术有哪些？")
print(result["answer"])
```

## 📖 RAG工作原理

RAG（Retrieval-Augmented Generation）是一种增强大语言模型的技术：

1. **文档预处理**：将文档加载并分割成小片段
2. **向量化**：使用embedding模型将文本转换为向量
3. **存储**：将向量存储在向量数据库中
4. **检索**：根据用户问题，检索最相关的文档片段
5. **生成**：将检索到的上下文和问题一起输入LLM，生成回答

### 工作流程

```
用户问题
    ↓
问题向量化
    ↓
检索相似文档 (向量相似度计算)
    ↓
构建上下文
    ↓
LLM生成回答
    ↓
返回答案 + 来源
```

## ⚙️ 配置参数

### SimpleRAG类参数

- `documents_path`: 文档目录路径（默认：`"./documents"`）
- `embedding_model`: 嵌入模型（默认：`"text-embedding-3-small"`）
- `llm_model`: LLM模型（默认：`"gpt-3.5-turbo"`）
- `temperature`: 温度参数，控制输出的随机性（0-1，默认：0.7）

### 文档分割参数

- `chunk_size`: 每个文档片段的字符数（默认：1000）
- `chunk_overlap`: 片段之间的重叠字符数（默认：200）

### 检索参数

- `k`: 检索相关文档的数量（默认：4）

## 🔧 进阶使用

### 更换模型

```python
# 使用GPT-4
rag = SimpleRAG(
    documents_path="./documents",
    llm_model="gpt-4",
    temperature=0.7
)

# 使用更大的嵌入模型
rag = SimpleRAG(
    documents_path="./documents",
    embedding_model="text-embedding-3-large"
)
```

### 调整检索参数

```python
# 检索更多相关文档
rag.create_qa_chain(k=8)

# 调整文档分割大小
split_docs = rag.split_documents(chunk_size=1500, chunk_overlap=300)
```

### 批量查询

```python
questions = [
    "文档的主要内容是什么？",
    "关键信息有哪些？",
    "有什么重要的数据？"
]

results = []
for q in questions:
    result = rag.query(q)
    results.append(result)
```

## 📝 示例输出

```
==================================================
开始初始化RAG系统
==================================================
正在初始化组件...
组件初始化完成！
正在从 ./documents 加载文档...
✓ 加载TXT: sample_document.txt
总共加载了 1 个文档片段
正在分割文档...
文档已分割为 5 个片段
正在创建向量存储...
向量存储已创建: ./vectorstore
向量存储中包含 5 个文档

正在创建问答链...
问答链创建完成！

==================================================
RAG系统初始化完成！
==================================================

问题: 什么是RAG？
--------------------------------------------------

回答: RAG是Retrieval-Augmented Generation的缩写，是一种结合了信息检索和生成式AI的技术。它通过检索相关文档来增强LLM的生成能力，提供更准确和相关的回答。

来源文档:
  [1] documents/sample_document.txt
       ## RAG技术

RAG（Retrieval-Augmented Generation）是一种结合了信息检索和生成式AI的技术...
```

## 🎓 学习要点

### 1. RAG的核心概念

- **检索（Retrieval）**：根据问题找到相关文档
- **增强（Augmented）**：使用检索到的信息增强提示
- **生成（Generation）**：基于增强的上下文生成回答

### 2. 关键组件理解

- **文本分割器**：将长文档切分为适合embedding的小块
- **向量数据库**：存储和检索文档向量
- **检索器**：基于相似度搜索相关文档
- **提示模板**：控制LLM如何处理检索到的上下文

### 3. 最佳实践

- ✅ 文档片段大小要适中（500-1500字符）
- ✅ 使用适当的重叠来保持上下文连贯性
- ✅ 选择合适的检索数量（k值）
- ✅ 设计好的提示模板来引导LLM
- ✅ 始终返回来源文档以提高可信度

## ❓ 常见问题

### Q: 如何添加新文档？

A: 只需将新的PDF或TXT文件放入 `documents/` 目录，然后重新运行程序即可。

### Q: 向量数据库可以重用吗？

A: 目前每次运行都会重新创建。你可以修改代码来加载已存在的向量数据库。

### Q: 支持其他格式的文档吗？

A: LangChain支持很多格式，如CSV、Markdown、网页等。你可以在代码中添加相应的加载器。

### Q: 如何减少API调用成本？

A: 可以缓存向量数据库，只在文档更新时重新生成。也可以使用更便宜的embedding模型。

## 📚 扩展阅读

- [LangChain官方文档](https://python.langchain.com/)
- [Chroma向量数据库](https://www.trychroma.com/)
- [RAG论文](https://arxiv.org/abs/2005.11401)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交问题和改进建议！

---

**Happy Coding with RAG! 🚀**
