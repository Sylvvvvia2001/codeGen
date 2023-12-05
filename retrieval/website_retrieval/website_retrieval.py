# 使用GPT-4 插件，MixerBox WebSearch
# 搜索 "name" conncetion method

import requests
import json
import os
import yaml

# 读取 YAML 文件
with open("../device_information.yaml", 'r') as file:
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
response_data = response.json()

# 提取 URL 并保存到文件
urls = [msg['content'] for msg in response_data['choices'][0]['message'] if msg['role'] == 'assistant']
with open("web_addr.txt", 'w') as file:
    for url in urls:
        file.write(url + "\n")
