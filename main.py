import argparse

from src.github_service import get_pull_request
from src.llm_service import review_code

def perform_review(repo_name: str, pr_number: int):
    """
    指定されたプルリクエストに対してコードレビューを実行し、コメントを投稿する
    """
    pr = get_pull_request(repo_name, pr_number)
    files = pr.get_files()

    review_comments = []
    for file in files:
        if file.status == 'removed':
            continue
        
        try:
            content_file = pr.base.repo.get_contents(file.filename, ref=pr.head.sha)
            code = content_file.decoded_content.decode('utf-8')
            review_result = review_code(code)
            comment = f"### `{file.filename}`\n\n{review_result}"
            review_comments.append(comment)
        except Exception as e:
            comment = f"### `{file.filename}`\n\nレビュー中にエラーが発生しました: {e}"
            review_comments.append(comment)

    if review_comments:
        final_comment = "# AI Code Review\n\n" + "\n\n---\n\n".join(review_comments)
        pr.create_issue_comment(final_comment)
        print("Successfully posted a review comment to the pull request.")
    else:
        print("No files to review.")

def main():
    """
    メイン処理 (CLIからの実行用)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_name", help="リポジトリ名 (e.g., 'owner/repo')")
    parser.add_argument("pr_number", type=int, help="プルリクエスト番号")
    args = parser.parse_args()

    perform_review(args.repo_name, args.pr_number)

if __name__ == "__main__":
    main()
