import requests
import json
import os
import yaml
# 不再需要正则表达式库，因为我们不提取 URL

def retrieve():
    # 读取 YAML 文件
    with open("retrieval/device_information.yaml", 'r') as file:
        device_info = yaml.safe_load(file)
    name = device_info['name']

    # 构造搜索查询
    search_query = f"{name}"

    # 读取 example.txt 文件
    with open("retrieval/api_retrieval/example.txt", 'r') as file:
        example_content = file.read()

    # API URL 和 Headers
    url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
    api_key = os.getenv('GPT_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }

    # 构造请求数据
    data = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are GPT-4, a large language model trained by OpenAI."
            },
            {
                "role": "user",
                "content": example_content  # 添加 example.txt 的内容作为上下文
            },
            {
                "role": "system",
                "content": f"Based on the specified thinking model, to implement the control code for {search_query}, search on the Internet (excepect the official website) to search of {search_query} to find some useful technical detail."
                f"You can serach in the IoT Blog of its brand or YouTube that whatever you think is useful."
                f"Tell me which way can be used to connect the device(like BlueTooth or ZigBee), which way can be used to control the device(like http or MQTT) and provide detailed usage or precise URLs of these manuals. "
                f"The types of technical method in manuals include, but are not limited to, connect protocol, how to get cloud information, among others."
            },
            {
                "role": "user",
                "content": f"search api for {search_query}, and return the api detail"
            }
        ],
        "temperature": 0.5
    }

    # 发送请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 检查响应状态码
    if response.status_code != 200:
        print("请求失败，状态码：", response.status_code)
        print(response.text)
        exit()

    response_data = response.json()

    # 确保 response_data['choices'] 是一个列表并且其中包含至少一个元素
    if 'choices' in response_data and len(response_data['choices']) > 0:
        # 获取完整的回答内容
        full_response = response_data['choices'][0]['message']['content']

        # 保存完整回答到文件
        with open("retrieval/website_retrieval/web_addr.txt", 'w') as file:
            file.write(full_response)

def main():
    retrieve()
    
if __name__ == "__main__":
    main()