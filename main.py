import os
import argparse
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def get_review_target_code(target_path: str) -> str:
    """
    レビュー対象のソースコードをファイルから読み込む
    """
    with open(target_path, 'r', encoding='utf-8') as f:
        return f.read()

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
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(code=code)

def main():
    """
    メイン処理
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("target_path", help="レビュー対象のソースコードのパス")
    args = parser.parse_args()

    # 出力ディレクトリを作成
    output_dir = "reviews"
    os.makedirs(output_dir, exist_ok=True)

    code = get_review_target_code(args.target_path)
    review_result = review_code(code)

    # レビュー結果をファイルに保存
    output_filename = os.path.basename(args.target_path) + ".md"
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Review for {os.path.basename(args.target_path)}\n\n")
        f.write(review_result)

    print(f"Review result saved to: {output_path}")
    print("\n--- Review Result ---")
    print(review_result)

if __name__ == "__main__":
    main()