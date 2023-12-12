import requests
import os
import json

# 设置API URL和API密钥
url = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
api_key = os.getenv('GPT_API_KEY')

headers = {
    "Content-Type": "application/json",
    "Authorization": api_key
}

# 准备请求数据
data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are a code generator, and generate Python code for smart devices"
        },
        {
            "role": "user",
            "content": f"You are a code generator."
            f"The files I provided named retrieval.txt shows some technical information to control the device. The file named lib.zip shows some relevant code in Gitee and Github. The file named base_platforms.zip or components.zip shows some command class, functions or sentences you might used in files with the file's name. "
            f"The file named device_information.yaml show the information of the Device. "
            f"Based on the basic information of a certain smart home device and some additional information I provide, which includes the device's connection method, connection protocol, APIs, etc., you need to generate a complete and executable Python project. "
            f"This project should enable me to control the smart device. If there is missing information that prevents you from completing a part of the code, please search online yourself. And list any required libraries that need to be downloaded in a requirements file, and provide this requirements file. "
            f"Once you believe the code you provided is complete and runnable, tell me 'The final code has been implemented,' and show me the code files."        }
    ],
    "temperature": 0.7
}

# 发送请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 打印并保存响应结果
print(response.json())
with open('code/origin_result.txt', 'w') as file:
    json.dump(response.json(), file)
