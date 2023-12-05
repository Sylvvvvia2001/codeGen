# main.py
import api_retrieval
import open_lib_retrieval
import file_retrieval
import website_retrieval

def main():
    # 调用 api_retrieval.py 中的函数
    api_retrieval.api_retrieval()

    # 调用 open_lib_retrieval.py 中的函数
    open_lib_retrieval.open_lib_retrieval()

    # 调用 file_retrieval.py 中的函数
    file_retrieval.file_retrieval()

    # 调用 website_retrieval.py 中的函数
    website_retrieval.website_retrieval()

if __name__ == "__main__":
    main()

