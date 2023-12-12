def read_file(file_path):
    """
    读取文本文件的内容
    :param file_path: 文件的路径
    :return: 文件的内容
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def combine_contents(api_text, web_text, file_text):
    """
    将三部分内容合并成一个字符串
    :param api_text: API小节的文本内容
    :param web_text: Web Content小节的文本内容
    :param file_text: Manual Information小节的文本内容
    :return: 合并后的内容
    """
    combined_text = "APIs\n" + api_text + "\n\n"
    combined_text += "Web Content\n" + web_text + "\n\n"
    combined_text += "Manual Information\n" + file_text
    return combined_text

def save_text(text, file_path):
    """
    将文本内容保存到文件
    :param text: 要保存的文本
    :param file_path: 文件的路径
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

def main():
    # 读取原始文本文件
    api_text = read_file("retrieval/api_retrieval/api_document_addr.txt")
    web_text = read_file("retrieval/website_retrieval/web_addr.txt")
    file_text = read_file("retrieval/file_retrieval/file_addr.txt")

    # 合并内容
    combined_text = combine_contents(api_text, web_text, file_text)

    # 保存到新的文本文件
    save_text(combined_text, "attach_knowledge/retireval.txt")

if __name__ == "__main__":
    main()
