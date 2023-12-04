import requests
import os
import yaml

# 设置当前工作目录为脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 读取GitHub Token和设备关键字
def get_github_token(file_path='github_token.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()

def get_device_keywords(file_path='../device_information.yaml'):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return [data['brand'], data['name'], data['type'], data['model']]

# 使用API对每个关键字进行搜索
def github_search(keyword, token):
    query = keyword + '+in:file'  # 搜索文件中的关键字
    url = f"https://api.github.com/search/code?q={query}"
    headers = {'Authorization': f'token {token}'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed for '{keyword}': " + response.text)

    return response.json()

# 解析并下载搜索到的文件
def download_files_from_search_results(results, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for item in results['items']:
        # 获取文件的RAW URL
        raw_url = item['html_url'].replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        file_path = os.path.join(target_folder, item['name'])
        
        # 下载文件
        response = requests.get(raw_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download file: {raw_url}")

# 主函数
def main():
    token = get_github_token()
    keywords = get_device_keywords()
    for keyword in keywords:
        search_results = github_search(keyword, token)
        if search_results['total_count'] > 0:
            download_files_from_search_results(search_results, "github_result")

if __name__ == '__main__':
    main()
