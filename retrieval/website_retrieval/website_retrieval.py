# 使用GPT-4 插件，MixerBox WebSearch
# 搜索 "name" conncetion method

import requests
import json
import os
import yaml
import re

def retrieve():

    # 读取 YAML 文件
    with open("retrieval/device_information.yaml", 'r') as file:
        device_info = yaml.safe_load(file)
    device_name = device_info['name']

    # 构造搜索查询
    search_query = f"{device_name} conncetion method"

    # API URL 和 Headers
    url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    api_key = os.getenv('GPT_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    # 构造请求数据
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": f"You are a browser tool. Search for '{search_query}' and return the top 20 results."
            },
            {
                "role": "user",
                "content": f"search {search_query}"
            }
        ],
        "temperature": 0.7
    }

    # 发送请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())

    # 检查响应状态码
    if response.status_code != 200:
        print("请求失败，状态码：", response.status_code)
        print(response.text)
        exit()

    response_data = response.json()

    # 确保 response_data['choices'] 是一个列表并且其中包含至少一个元素
    if 'choices' in response_data and len(response_data['choices']) > 0:
        # 直接获取 message 字段
        message_content = response_data['choices'][0]['message']['content']
        
        # 使用正则表达式提取 URL (支持 http 和 https)
        urls = re.findall(r"http[s]?://\S+", message_content)

        # 保存 URLs 到文件
        with open("retrieval/website_retrieval/web_addr.txt", 'w') as file:
            for url in urls:
                file.write(url + "\n")

def main():
    retrieve()

if __name__ == "__main__":
    main()