import requests
import os
import yaml

def get_gitee_token(file_path='retrieval/open_lib_retrieval/gitee_token.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()

def get_device_keywords(file_path='retrieval/device_information.yaml'):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return [data[key] for key in ['brand', 'name', 'type', 'model']]

def search_repositories_with_keywords(keywords, token):
    for keyword in keywords:
        url = "https://gitee.com/api/v5/search/repositories"
        params = {'access_token': token, 'q': keyword}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print(f"根据关键词 '{keyword}' 搜索仓库成功。")
            for item in response.json():
                yield item['full_name']
        else:
            print(f"根据关键词 '{keyword}' 搜索仓库失败：{response.text}")

def download_files_from_repo(repo_full_name, keywords, token, target_folder):
    # 获取仓库的文件树
    tree_url = f"https://gitee.com/api/v5/repos/{repo_full_name}/git/trees/master?recursive=1&access_token={token}"
    response = requests.get(tree_url)
    if response.status_code == 200:
        tree = response.json()
        print(f"成功获取仓库 '{repo_full_name}' 的文件树。")
        
        # 查找匹配关键词的文件或目录
        for node in tree['tree']:
            if any(keyword.lower() in node['path'].lower() for keyword in keywords):
                # 分离仓库名和路径，然后安全地拼接它们
                repo_parts = repo_full_name.split('/')
                path_parts = node['path'].split('/')
                file_dir = os.path.join(target_folder, *repo_parts, *path_parts[:-1])

                try:
                    os.makedirs(file_dir, exist_ok=True)
                except OSError as e:
                    print(f"创建目录失败：{e}")
                    continue  # 如果创建目录失败，则跳过当前文件
                
                # 构建文件的完整本地路径
                file_path = os.path.join(target_folder, repo_full_name, node['path'])
                file_dir = os.path.dirname(file_path)
                # 检查路径是否存在，以及它是否不是一个文件
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                elif os.path.isfile(file_dir):
                    print(f"错误：路径 '{file_dir}' 是一个文件，无法创建同名的文件夹。")
                    continue  # 跳过这个节点，继续下一个
                # 使用内容 API 来获取文件
                contents_url = f"https://gitee.com/api/v5/repos/{repo_full_name}/contents/{node['path']}?ref=master&access_token={token}"
                contents_response = requests.get(contents_url)
                if contents_response.status_code == 200:
                    # 下载文件内容
                    with open(file_path, 'wb') as file:
                        file.write(contents_response.content)
                    print(f"成功下载文件：'{node['path']}'。")
                else:
                    print(f"下载文件失败：'{node['path']}'。")
    else:
        print(f"获取仓库 '{repo_full_name}' 的文件树失败：{response.text}")



def main():
    token = get_gitee_token()
    keywords = get_device_keywords()
    target_folder = 'retrieval/open_lib_retrieval/gitee_result'
    os.makedirs(target_folder, exist_ok=True)

    for repo_full_name in search_repositories_with_keywords(keywords, token):
        download_files_from_repo(repo_full_name, keywords, token, target_folder)

if __name__ == '__main__':
    main()
