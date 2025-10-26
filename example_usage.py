#!/usr/bin/env python3
"""
RAG演示项目的示例使用代码
"""

from rag_demo import SimpleRAG

def main():
    # 创建RAG实例
    rag = SimpleRAG(
        documents_path="./documents",
        embedding_model="text-embedding-3-small",
        llm_model="gpt-3.5-turbo",
        temperature=0.7
    )
    
    # 初始化系统
    rag.initialize_full_system()
    
    # 交互式查询
    print("\\n" + "=" * 50)
    print("RAG系统已就绪！输入问题开始查询，输入'quit'退出")
    print("=" * 50 + "\\n")
    
    while True:
        question = input("请输入您的问题: ")
        
        if question.lower() in ['quit', 'exit', '退出']:
            print("再见！")
            break
        
        if not question.strip():
            continue
        
        try:
            rag.query(question)
        except Exception as e:
            print(f"查询时出错: {str(e)}")

if __name__ == "__main__":
    main()
