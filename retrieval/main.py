# main.py
from api_retrieval.api_retrieval import main as api_retrieval
from file_retrieval.file_retrieval import main as file_retrieval
from open_lib_retrieval.gitee_search import main as gitee_search
from open_lib_retrieval.github_search import main as github_search
from website_retrieval.website_retrieval import main as website_retrieval


def main():
    # 调用 api_retrieval.py 中的函数
    api_retrieval()

    # 调用 file_retrieval.py 中的函数
    file_retrieval()

    # 调用 website_retrieval.py 中的函数
    website_retrieval()

    # 调用 open_lib_retrieval.py 中的函数
    gitee_search()
    github_search()

if __name__ == "__main__":
    main()

