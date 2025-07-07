import os
from github import Github, Auth
from dotenv import load_dotenv

def get_github_client() -> Github:
    """
    GitHub APIクライアントを取得する
    """
    load_dotenv()
    # Read the private key from the file
    with open("private-key.pem", "r") as f:
        private_key = f.read()
        
    auth = Auth.AppAuth(
        os.environ["GITHUB_APP_ID"],
        private_key,
    ).get_installation_auth(int(os.environ["GITHUB_INSTALLATION_ID"]))
    return Github(auth=auth)

def get_pull_request(repo_name: str, pr_number: int):
    """
    リポジトリ名とPR番号からプルリクエストオブジェクトを取得する
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)
    return repo.get_pull(pr_number)
