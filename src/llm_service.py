import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_prompt() -> PromptTemplate:
    """
    レビューを依頼するためのプロンプトを作成する
    """
    template = """
あなたはプロのソフトウェアエンジニアです。
以下のソースコードをレビューして、改善点を指摘してください。

観点：
- セキュリティ
- パフォーマンス
- 可読性
- バグの可能性

ソースコード：
{code}
"""
    return PromptTemplate(template=template, input_variables=["code"])

def review_code(code: str) -> str:
    """
    LangChainのAzureChatOpenAIを使用して、ソースコードレビューを実行する
    """
    load_dotenv()
    llm = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    )
    prompt = create_prompt()
    # LCEL (LangChain Expression Language) を使用した新しい書き方
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"code": code})
