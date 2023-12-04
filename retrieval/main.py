import api_retrieval
import open_lib_retrieval
import file_retrieval
import website_retrieval

def main():
    # 调用IOT API文档检索模块
    api_results = api_retrieval.retrieve_api_docs()
    with open('api_results.txt', 'w', encoding='utf-8') as f:
        f.write(api_results)

    # 调用开源库代码检索模块
    lib_results = open_lib_retrieval.retrieve_open_libs()
    with open('lib_results.txt', 'w', encoding='utf-8') as f:
        f.write(lib_results)

    # 调用产品手册检索模块
    file_results = file_retrieval.retrieve_manuals()
    with open('file_results.txt', 'w', encoding='utf-8') as f:
        f.write(file_results)

    # 调用网页内容检索模块
    website_results = website_retrieval.retrieve_web_content()
    with open('website_results.txt', 'w', encoding='utf-8') as f:
        f.write(website_results)

if __name__ == "__main__":
    main()
