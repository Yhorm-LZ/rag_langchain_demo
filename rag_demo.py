"""
RAG (Retrieval-Augmented Generation) 演示项目
集成LangChain LLM使用
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate
from typing import List

load_dotenv()

# 全局设置Ollama主机地址（在模块加载时）
os.environ['OLLAMA_HOST'] = 'http://localhost:11434'

class SimpleRAG:
    def __init__(self, documents_path: str, embedding_model: str = "nomic-embed-text", llm_model: str = "llama3:8b", temperature: float = 0.7, use_ollama: bool = True):
        self.documents_path = documents_path
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.temperature = temperature
        self.use_ollama = use_ollama
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.qa_chain = None
        self.documents = []
    
    def initialize_components(self):
        print("正在初始化组件...")
        if self.use_ollama:
            # 使用Ollama本地模型
            print("使用Ollama本地模型...")
            
            # 使用正确的Ollama地址
            ollama_url = "http://localhost:11434"
            
            self.llm = ChatOllama(
                model=self.llm_model,
                temperature=self.temperature,
                base_url=ollama_url
            )
            self.embeddings = OllamaEmbeddings(
                model=self.embedding_model,
                base_url=ollama_url
            )
        else:
            # 使用OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("请在.env文件中设置OPENAI_API_KEY")
            self.llm = ChatOpenAI(model_name=self.llm_model, temperature=self.temperature, openai_api_key=api_key)
            self.embeddings = OpenAIEmbeddings(model=self.embedding_model, openai_api_key=api_key)
        print("组件初始化完成！")
    
    def load_documents(self) -> List:
        print(f"正在从 {self.documents_path} 加载文档...")
        if not os.path.exists(self.documents_path):
            raise ValueError(f"文档路径不存在: {self.documents_path}")
        all_documents = []
        for file_name in os.listdir(self.documents_path):
            file_path = os.path.join(self.documents_path, file_name)
            if file_name.startswith('.') or os.path.isdir(file_path):
                continue
            try:
                if file_name.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    all_documents.extend(docs)
                    print(f"✓ 加载PDF: {file_name}")
                elif file_name.endswith('.txt'):
                    loader = TextLoader(file_path, encoding='utf-8')
                    docs = loader.load()
                    all_documents.extend(docs)
                    print(f"✓ 加载TXT: {file_name}")
            except Exception as e:
                print(f"✗ 加载 {file_name} 时出错: {str(e)}")
                continue
        self.documents = all_documents
        print(f"总共加载了 {len(self.documents)} 个文档片段")
        return self.documents
    
    def split_documents(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        print("正在分割文档...")
        if not self.documents:
            raise ValueError("没有文档可以分割，请先加载文档")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len)
        split_docs = text_splitter.split_documents(self.documents)
        print(f"文档已分割为 {len(split_docs)} 个片段")
        return split_docs
    
    def create_vectorstore(self, documents: List, persist_directory: str = "./vectorstore"):
        print("正在创建向量存储...")
        if not documents:
            raise ValueError("没有文档可以向量化")
        
        try:
            # 使用手动方法避免embed_documents问题
            print("为文档生成embeddings...")
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            # 逐个生成embeddings，同时过滤文本和元数据
            embeddings = []
            filtered_texts = []
            filtered_metadatas = []
            
            for i, text in enumerate(texts, 1):
                print(f"  处理文档 {i}/{len(texts)} (长度: {len(text)} 字符)")
                try:
                    emb = self.embeddings.embed_query(text)
                    embeddings.append(emb)
                    filtered_texts.append(text)
                    filtered_metadatas.append(metadatas[i-1])  # i是从1开始的
                except Exception as e:
                    print(f"  ✗ 文档 {i} 失败: {e}")
                    print(f"  前50字符: {text[:50]}")
                    # 跳过这个文档
                    continue
            
            print(f"✓ 成功生成 {len(embeddings)} 个embeddings")
            
            # 验证长度一致性
            assert len(embeddings) == len(filtered_texts) == len(filtered_metadatas), \
                f"长度不一致: embeddings={len(embeddings)}, texts={len(filtered_texts)}, metadatas={len(filtered_metadatas)}"
            
            # 使用from_embeddings创建向量存储
            print("创建FAISS向量存储...")
            self.vectorstore = FAISS.from_embeddings(
                text_embeddings=list(zip(filtered_texts, embeddings)),
                embedding=self.embeddings,
                metadatas=filtered_metadatas
            )
            
        except Exception as e:
            print(f"\n向量化时出错: {str(e)}")
            print("\n💡 建议切换到OpenAI模式")
            print("修改 main() 函数中的 use_ollama = False")
            import traceback
            traceback.print_exc()
            raise
        
        self.vectorstore.save_local(persist_directory)
        print(f"向量存储已创建: {persist_directory}")
        print(f"向量存储中包含 {len(documents)} 个文档")
    
    def create_qa_chain(self, k: int = 4):
        print("正在创建问答链...")
        if not self.vectorstore:
            raise ValueError("向量存储未创建，请先创建向量存储")
        prompt_template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要编造答案。

{context}

问题: {question}
答案: """
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=retriever, chain_type_kwargs={"prompt": PROMPT}, return_source_documents=True)
        print("问答链创建完成！")
    
    def query(self, question: str):
        if not self.qa_chain:
            raise ValueError("问答链未创建，请先创建问答链")
        print(f"\n问题: {question}")
        print("-" * 50)
        result = self.qa_chain.invoke({"query": question})
        answer = result["result"]
        sources = result["source_documents"]
        print(f"\n回答: {answer}")
        print("\n来源文档:")
        for i, doc in enumerate(sources, 1):
            print(f"  [{i}] {doc.metadata.get('source', 'Unknown')}")
            print(f"       {doc.page_content[:100]}...")
        return {"answer": answer, "sources": [{"content": doc.page_content, "metadata": doc.metadata} for doc in sources]}
    
    def initialize_full_system(self):
        print("=" * 50)
        print("开始初始化RAG系统")
        print("=" * 50)
        self.initialize_components()
        self.load_documents()
        # 使用更小的chunk_size获得更细粒度的知识块
        split_docs = self.split_documents(chunk_size=300, chunk_overlap=50)
        self.create_vectorstore(split_docs)
        self.create_qa_chain()
        print("\n" + "=" * 50)
        print("RAG系统初始化完成！")
        print("=" * 50)
        print()

def main():
    documents_path = "./documents"
    # 使用Ollama模式（当前有连接问题，暂时使用OpenAI）
    use_ollama = True  # 设置为True使用Ollama，False使用OpenAI
    
    if use_ollama:
        # Ollama本地模型配置
        embedding_model = "nomic-embed-text"  # 推荐embedding模型
        llm_model = "llama3:8b"  # 推荐对话模型
        print("🎯 使用Ollama本地模型")
        print(f"   Embedding模型: {embedding_model}")
        print(f"   LLM模型: {llm_model}")
    else:
        # OpenAI配置
        embedding_model = "text-embedding-3-small"
        llm_model = "gpt-3.5-turbo"
        print("🌐 使用OpenAI模型")
    
    rag = SimpleRAG(
        documents_path=documents_path, 
        embedding_model=embedding_model, 
        llm_model=llm_model, 
        temperature=0.7,
        use_ollama=use_ollama
    )
    rag.initialize_full_system()
    questions = ["使用了RAG后,回答质量不佳怎么办"]
    print("\n开始测试查询...")
    print("=" * 50)
    for question in questions:
        try:
            rag.query(question)
            print("\n" + "=" * 50 + "\n")
        except Exception as e:
            print(f"查询时出错: {str(e)}\n")

if __name__ == "__main__":
    main()
